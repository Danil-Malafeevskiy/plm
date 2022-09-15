from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.utils import timezone

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

        feature_old = {feature.id: feature for feature in instance}
        feature_update = [feature for feature in validated_data if 'id' in feature.keys()]

        update_id = [feature['id'] for feature in validated_data if 'id' in feature.keys()]

        features = [feature for feature in validated_data if 'id' not in feature.keys()]
        for feature in features:
            self.child.create(feature)

        res_update = []
        for obj_feature in feature_update:

            feature = feature_old.get(obj_feature['id'])
            type = FeatureSerializer(feature).data['geometry']
            if type['type'] == 'Point':
                for line in self.context:
                    for lineIndex in range(len(line['geometry']['coordinates'])):
                        if type['coordinates'] == line['geometry']['coordinates'][lineIndex]:
                            line['geometry']['coordinates'][lineIndex] = FeatureSerializer(obj_feature).data['geometry']['coordinates']
                            break
                    new_line = FeatureSerializer(Feature.objects.get(id=line['id']), data=line)
                    if new_line.is_valid():
                        new_line.save()
            res_update.append(obj_feature)
            self.child.update(feature, obj_feature)

        for feature_id, feature in feature_old.items():
            if feature_id not in update_id:
                type = FeatureSerializer(feature).data['geometry']
                if type['type'] == 'Point':
                    for line in self.context:
                        lineCoord = []
                        for lineIndex in range(len(line['geometry']['coordinates'])):
                            if type['coordinates'] != line['geometry']['coordinates'][lineIndex]:
                                lineCoord.append(line['geometry']['coordinates'][lineIndex])
                        line['geometry']['coordinates'] = lineCoord

                        if len(line['geometry']['coordinates']) <= 1:
                            Feature.objects.get(id=line['id']).delete()
                        else:
                            new_line = FeatureSerializer(Feature.objects.get(id=line['id']), data=line)
                            if new_line.is_valid():
                                new_line.save()
                feature.delete()

        return res_update

class FeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    geometry = GeometryField()
    image = BinaryField(required=False)
    class Meta:
        ordering = ['id']
        list_serializer_class = FeatureListSerializer
        geo_field = 'geometry'
        model = Feature
        fields = ('id', 'name', 'type', 'properties', 'geometry', 'image')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(FeatureSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    avaible_permissions = serializers.SerializerMethodField()
    class Meta:
        ordering = ['id']
        model = Group
        fields = ('id', 'name', 'permissions', 'avaible_permissions')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(GroupSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

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
    class Meta:
        ordering = ['id']
        model = Type
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group', 'avaible_group')
        validators = [
            UniqueTogetherValidator(
                queryset=Type.objects.all(),
                fields=['name']
            )
        ]

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TypeSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

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