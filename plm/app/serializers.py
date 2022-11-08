from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers, exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_gis.serializers import GeometryField
import django.contrib.auth.password_validation as validators

from plm import settings
from app.models import Feature, Type, VersionControl, Ruls
from django.contrib.auth import get_user_model

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return bytes(value).decode('utf-8')

    def to_internal_value(self, value):
         return value.encode('utf-8')

class FeatureListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):

        version = {"create": [], "update": [], "delete": []}
        new_version = {"create": [], "update": [], "delete": []}

        feature_old = {feature.id: feature for feature in instance}
        feature_update = [feature for feature in validated_data if 'id' in feature.keys() and feature['id'] in feature_old.keys()]

        update_id = [feature['id'] for feature in validated_data if 'id' in feature.keys() and feature['id'] in feature_old.keys()]

        features = [feature for feature in validated_data if 'id' not in feature.keys() or feature['id'] not in feature_old.keys()]

        for feature in features:
            obj = FeatureSerializer(self.child.create(feature)).data
            new_version['create'].append(obj)
            version['delete'].append(obj['id'])

        up_dict = {}
        new_line_dict = {}
        for obj_feature in feature_update:
            feature = feature_old.get(obj_feature['id'], None)
            if (feature!=None):
                type = FeatureSerializer(feature).data
                if self.context!=False and type['geometry']['type'] == 'Point' and (type['geometry']['coordinates']!=FeatureSerializer(obj_feature).data['geometry']['coordinates']):
                    for line in self.context:
                        up_flag = False
                        copy_line = FeatureSerializer(Feature.objects.get(id=line['id'])).data
                        for lineIndex in range(len(line['geometry']['coordinates'])):
                            if type['geometry']['coordinates'] == line['geometry']['coordinates'][lineIndex]:
                                line['geometry']['coordinates'][lineIndex] = FeatureSerializer(obj_feature).data['geometry']['coordinates']
                                up_flag = True
                                break
                        if up_flag:
                            feat = Feature.objects.get(id=line['id'])
                            feat.geometry = GEOSGeometry(f'{line["geometry"]}')
                            feat.save()
                            if copy_line['id'] not in up_dict.keys():
                                up_dict[copy_line['id']] = copy_line
                            new_line_dict[copy_line['id']] = line['geometry']

                new_version['update'].append(FeatureSerializer(obj_feature).data)
                version['update'].append(type)
                if obj_feature['geometry'].geom_type == 'LineString':
                    if obj_feature['id'] not in up_dict.keys():
                        up_dict[obj_feature['id']] = type
                if obj_feature['id'] in new_line_dict.keys():
                    obj_feature['geometry'] = GEOSGeometry(f'{new_line_dict[obj_feature["id"]]}')
                self.child.update(feature, obj_feature)

        del_line = []

        for feature_id, feature in feature_old.items():
            if feature_id not in update_id:
                type = FeatureSerializer(feature).data
                if self.context != False and type['geometry']['type'] == 'Point':
                    for line in self.context:
                        lineCoord = []
                        del_flag = False
                        try:
                            copy_line = FeatureSerializer(Feature.objects.get(id=line['id'])).data
                        except Exception:
                            continue
                        for lineIndex in range(len(line['geometry']['coordinates'])):
                            if type['geometry']['coordinates'] != line['geometry']['coordinates'][lineIndex]:
                                lineCoord.append(line['geometry']['coordinates'][lineIndex])
                            else:
                                del_flag = True
                        if del_flag and line['id'] not in new_version['delete']:
                            line['geometry']['coordinates'] = lineCoord

                            if len(line['geometry']['coordinates']) <= 1:
                                Feature.objects.get(id=line['id']).delete()
                                if line['id'] not in del_line:
                                    del_line.append(line['id'])
                                    new_version['delete'].append(line['id'])
                            else:
                                feat = Feature.objects.get(id=line['id'])
                                feat.geometry = GEOSGeometry(f'{line["geometry"]}')
                                feat.save()

                            if copy_line['id'] not in up_dict.keys():
                                up_dict[copy_line['id']] = copy_line

                if feature_id not in new_version['delete']:
                    version['create'].append(type)
                    new_version['delete'].append(feature_id)
                    feature.delete()

        if (len(up_dict)!=0 or len(del_line)!=0) and self.context!=False:
            for line in self.context:
                if line['id'] in del_line:
                    version['create'].append(up_dict[line['id']])
                elif line['id'] in up_dict.keys() and line['id'] not in new_version['delete']:
                    flag_find = False
                    for obj in new_version['update']:
                        if obj['id'] == line['id']:
                            obj['geometry']['coordinates'] = line['geometry']['coordinates']
                            flag_find = True
                            break
                    if not flag_find:
                        version['update'].append(up_dict[line['id']])
                        new_version['update'].append(line)

        new_update = []
        old_update = []
        if self.context!=False:
            for index in range(len(new_version['update'])):
                if new_version['update'][index]['id'] not in new_version['delete']:
                    new_update.append(new_version['update'][index])

                if version['update'][index]['id'] not in new_version['delete']:
                    old_update.append(version['update'][index])
            new_version['update'] = new_update
            version['update'] = old_update

        return version, new_version

class FeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    geometry = GeometryField()
    group = serializers.SerializerMethodField()
    image = BinaryField(required=False)
    class Meta:
        ordering = ['id']
        list_serializer_class = FeatureListSerializer
        geo_field = 'geometry'
        model = Feature
        fields = ('id', 'name', 'type', 'properties', 'geometry', 'image', 'group')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(FeatureSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_group(self, obj):
        try:
            return obj.name.group.name
        except Exception:
            return obj['name'].group.name

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    group = serializers.CharField()
    filename = serializers.CharField()

class GroupSerializer(serializers.ModelSerializer):
    all_user = serializers.SerializerMethodField()
    all_type = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    class Meta:
        ordering = ['id']
        model = Group
        fields = ('id', 'name', 'all_user', 'all_type', 'users')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(GroupSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_all_user(self, obj):
        return len(get_user_model().objects.filter(groups__name=obj.name).exclude(id=self.context))

    def get_all_type(self, obj):
        return len(Type.objects.filter(group=obj.id))

    def get_users(self, obj):
        return list(get_user_model().objects.filter(groups=obj).exclude(id=self.context).values_list('username', flat=True))

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    avaible_permission = serializers.SerializerMethodField()
    image = BinaryField(required=False)
    user_permissions = serializers.SerializerMethodField()
    all_users = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)

    class Meta:
        ordering = ['id']
        model = get_user_model()
        validators = [
            UniqueTogetherValidator(
                queryset=get_user_model().objects.all(),
                fields=['email'],
                message="Такой email уже существует!"
            )
        ]
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'groups',
                  'permissions', 'avaible_permission', 'image', 'user_permissions', 'full_name', 'all_users')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_full_name(self, obj):
        return get_user_model().objects.get(username=obj.username).get_full_name()

    def get_groups(self, obj):
        if obj.is_superuser:
            return list(Group.objects.values_list('name', flat=True))

        return [group for group in list(obj.groups.values_list('name', flat=True))
                if group != "Admin"]

    def get_permissions(self, obj):
        return list(obj.user_permissions.values_list('name', flat=True))

    def get_avaible_permission(self, obj):
        perm = list(obj.user_permissions.values_list('name', flat=True))
        return [per.name for per in
                Permission.objects.filter(content_type_id=5).exclude(name__in=["Can add feature", "Can change feature", "Can delete feature", "Can view feature"])
                if per.name not in perm]

    def get_user_permissions(self, obj):
        perm = []
        if obj.is_superuser:
            return [perms.name for perms in Permission.objects.filter(content_type_id=5).exclude(name__in=["Can add feature", "Can change feature", "Can delete feature", "Can view feature"])]
        for group in obj.groups.values_list('name', flat=True):
            if group != "Admin":
                perm.append(f'Изменение объектов {group}')
                perm.append(f'Просмотр объектов {group}')
        return perm

    def get_all_users(self, obj):
        if obj.is_superuser:
            return list(get_user_model().objects.all().exclude(
                id=obj.id).values_list('username', flat=True))
        if obj.is_staff:
            return list(get_user_model().objects.all().exclude(groups=Group.objects.get(name="Admin")).exclude(
                id=obj.id).values_list('username', flat=True))
        return []

    def validate(self, data):
        if 'password' in data.keys():
            password = data.get('password')

            try:
                validators.validate_password(password=password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({"password": list(e.messages)})

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        user = super(UserSerializer, self).create(validated_data)

        for perm in self.context['permissions']:
            user.user_permissions.add(Permission.objects.get(name=perm))

        for group in self.context['groups']:
            user.groups.add(Group.objects.get(name=group))

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data.keys():
            validated_data['password'] = make_password(validated_data.get('password'))
            return super(UserSerializer, self).update(instance, validated_data)

        user = super(UserSerializer, self).update(instance, validated_data)

        user.user_permissions.clear()
        user.groups.clear()
        for perm in self.context['permissions']:
            user.user_permissions.add(Permission.objects.get(name=perm))

        for group in self.context['groups']:
            user.groups.add(Group.objects.get(name=group))

        return user

class TypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    group = serializers.SerializerMethodField()
    properties = serializers.JSONField(required=False, default=[""])
    image = BinaryField(required=False)
    all_obj = serializers.SerializerMethodField()
    all_group_type = serializers.SerializerMethodField()
    group_type = serializers.SerializerMethodField()
    class Meta:
        ordering = ['id']
        model = Type
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group', 'all_obj', 'all_group_type', 'group_type')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TypeSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def validate(self, data):
        if 'id' in data.keys():
            name = Type.objects.get(id=data['id']).name
            if name == data['name']:
                return super(TypeSerializer, self).validate(data)

        queryset = Type.objects.filter(group=Group.objects.get(name=self.context['group']), name=data['name'])
        if len(queryset)!=0:
            raise serializers.ValidationError({"name": "У этого датасета уже существует тип с таким именем!"})

        return super(TypeSerializer, self).validate(data)

    def get_all_group_type(self, obj):
        return list(Type.objects.filter(group=obj.group).exclude(id=obj.id).values_list('name', flat=True))

    def get_group_type(self, obj):
        return [type.type_2.name for type in Ruls.objects.filter(type_1=obj).exclude(type_2=obj)]

    def get_all_obj(self, obj):
        return len(Feature.objects.filter(name=obj.id))

    def get_group(self, obj):
        return Group.objects.get(id=obj.group_id).name

    def create(self, validated_data):
        validated_data['group'] = Group.objects.get(name=self.context['group'])
        type = super(TypeSerializer, self).create(validated_data)
        for ruls in self.context['ruls']:
            type_new = Type.objects.get(name=ruls, group=validated_data['group'])
            Ruls.objects.create(type_1=type, type_2=type_new)
            Ruls.objects.create(type_1=type_new, type_2=type)
        Ruls.objects.create(type_1=type, type_2=type)
        return type

    def update(self, instance, validated_data):
        validated_data['group'] = Group.objects.get(name=self.context['group'])
        type = super(TypeSerializer, self).update(instance, validated_data)
        ruls_1 = [type.type_2.name for type in Ruls.objects.filter(type_1=type).exclude(type_1=type, type_2=type)]
        for ruls in self.context['ruls']:
            type_new = Type.objects.get(name=ruls, group=validated_data['group'])
            if not Ruls.objects.filter(type_1=type, type_2=type_new).exists():
                Ruls.objects.create(type_1=type, type_2=type_new)
                Ruls.objects.create(type_1=type_new, type_2=type)
            else:
                ruls_1.remove(type_new.name)
        for r in ruls_1:
            type_new = Type.objects.get(name=r, group=validated_data['group'])
            Ruls.objects.get(type_1=type_new, type_2=type).delete()
            Ruls.objects.get(type_1=type, type_2=type_new).delete()
        return type

class VersionControlSerializer(serializers.ModelSerializer):
    date_update = serializers.DateTimeField(required=False, default=timezone.now, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        ordering = ['id']
        model = VersionControl
        fields = ('id', 'user', 'date_update', 'version', 'comment', 'dataset', 'version', 'new_version', 'flag', 'disabled')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(VersionControlSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=18, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        id = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed("Невалидный токен!")

        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        user.set_password(password)
        user.save()

        send_mail('Новый пароль', f'Ваш пароль быд изменен на: {password}',
                  settings.DEFAULT_FROM_EMAIL, [user.email])

        return super().validate(attrs)