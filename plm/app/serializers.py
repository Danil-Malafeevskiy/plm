from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_gis.serializers import GeometryField
import django.contrib.auth.password_validation as validators
from app.models import Feature, Dataset

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return bytes(value).decode('utf-8')

    def to_internal_value(self, value):
         return value.encode('utf-8')

class FeatureListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):

        feature_old = {feature.id: feature for feature in instance}
        feature_new = {feature['id']: feature for feature in validated_data}

        ret = []
        for feature_id, data in feature_new.items():
            feature = feature_old.get(feature_id, None)
            ret.append(self.child.update(feature, data))

        return ret

class FeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    geometry = GeometryField()
    image = BinaryField(required=False)
    class Meta:
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
        model = Group
        fields = ('id', 'name', 'permissions', 'avaible_permissions')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(GroupSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_permissions(self, obj):
        return list(obj.permissions.values_list('name', flat=True))

    def get_avaible_permissions(self, obj):
        perm = list(obj.permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm]

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

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups', 'avaible_group',
                  'permissions', 'avaible_permission', 'last_login', 'date_joined')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def get_permissions(self, obj):
        return list(obj.user_permissions.values_list('name', flat=True))

    def get_avaible_group(self, obj):
        perm = list(obj.groups.values_list('name', flat=True))
        return [per for per in Group.objects.all().values_list('name', flat=True)
                if per not in perm]

    def get_avaible_permission(self, obj):
        perm = list(obj.user_permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm]

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

class DatasetSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    avaible_group = serializers.SerializerMethodField()
    properties = serializers.JSONField(required=False, default=[""])
    image = serializers.CharField(required=False, default="", allow_blank=True)
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group', 'avaible_group')
        validators = [
            UniqueTogetherValidator(
                queryset=Dataset.objects.all(),
                fields=['name']
            )
        ]

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(DatasetSerializer, self).__init__(*args, **kwargs)

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
        return super(DatasetSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['group'] = Group.objects.get(name=self.context['group'])
        return super(DatasetSerializer, self).update(instance, validated_data)