from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_gis.serializers import GeometryField
import django.contrib.auth.password_validation as validators
from app.models import Feature, Type, VersionControl
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
                        copy_line = FeatureSerializer(Feature.objects.get(id=line['id'])).data
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

        if len(up_dict)!=0 or len(del_line)!=0 and self.context!=False:
            for line in self.context:
                if line['id'] in del_line:
                    version['create'].append(up_dict[line['id']])
                elif line['id'] in up_dict.keys() and line['id'] not in new_version['delete']:
                    for obj in new_version['update']:
                        if obj['id'] == line['id']:
                            obj['geometry']['coordinates'] = line['geometry']['coordinates']
                            break
                    else:
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

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    avaible_permissions = serializers.SerializerMethodField()
    all_user = serializers.SerializerMethodField()
    class Meta:
        ordering = ['id']
        model = Group
        fields = ('id', 'name', 'permissions', 'avaible_permissions', 'all_user')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(GroupSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_all_user(self, obj):
        return len(get_user_model().objects.filter(groups__name=obj.name))

    def get_permissions(self, obj):
        return [per for per in obj.permissions.values_list('name', flat=True)
                if "change" in per or "view" in per]

    def get_avaible_permissions(self, obj):
        perm = list(obj.permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm and ("change" in per or "view" in per)]

    def create(self, validated_data):
        group = super(GroupSerializer, self).create(validated_data)

        for perm in self.context['permissions']:
            group.permissions.add(Permission.objects.get(name=perm))

        return group

    def update(self, instance, validated_data):
        group = super(GroupSerializer, self).update(instance, validated_data)

        group.permissions.clear()
        for perm in self.context['permissions']:
            group.permissions.add(Permission.objects.get(name=perm))

        return group

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    avaible_group = serializers.SerializerMethodField()
    avaible_permission = serializers.SerializerMethodField()
    image = BinaryField(required=False)

    class Meta:
        ordering = ['id']
        model = get_user_model()
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups', 'avaible_group',
                  'permissions', 'avaible_permission', 'last_login', 'date_joined', 'image')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def get_permissions(self, obj):
        return [per for per in obj.user_permissions.values_list('name', flat=True)
                if "change" in per or "view" in per]

    def get_avaible_group(self, obj):
        perm = list(obj.groups.values_list('name', flat=True))
        return [per for per in Group.objects.all().values_list('name', flat=True)
                if per not in perm]

    def get_avaible_permission(self, obj):
        perm = list(obj.user_permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm or ("change" in per or "view" in per)]

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
    group = serializers.SerializerMethodField()
    avaible_group = serializers.SerializerMethodField()
    properties = serializers.JSONField(required=False, default=[""])
    image = BinaryField(required=False)
    all_obj = serializers.SerializerMethodField()
    name = serializers
    class Meta:
        ordering = ['id']
        model = Type
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group', 'avaible_group', 'all_obj')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TypeSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def validate(self, data):
        queryset = Type.objects.filter(group=Group.objects.get(name=self.context['group']), name=data['name'])
        if len(queryset)!=0:
            raise serializers.ValidationError({"name": "У этого датасета уже существует тип с таким именем!"})

        return super(TypeSerializer, self).validate(data)

    def get_all_obj(self, obj):
        return len(Feature.objects.filter(name=obj.id))

    def get_group(self, obj):
        return Group.objects.get(id=obj.group_id).name

    def get_avaible_group(self, obj):
        return [per for per in Group.objects.all().values_list('name', flat=True)
                if (per != Group.objects.get(id=obj.group_id).name)]

    def create(self, validated_data):
        validated_data['group'] = Group.objects.get(name=self.context['group'])
        return super(TypeSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['group'] = Group.objects.get(name=self.context['group'])
        return super(TypeSerializer, self).update(instance, validated_data)

class VersionControlSerializer(serializers.ModelSerializer):
    date_update = serializers.DateTimeField(required=False, default=timezone.now, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        ordering = ['id']
        model = VersionControl
        fields = ('id', 'user', 'date_update', 'version', 'comment', 'dataset', 'version', 'new_version', 'flag')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(VersionControlSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)