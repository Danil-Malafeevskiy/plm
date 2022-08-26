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

class FeatureSerializer(serializers.ModelSerializer):
    geometry = GeometryField()
    image = BinaryField()
    class Meta:
        geo_field = 'geometry'
        model = Feature
        fields = ('id', 'name', 'type', 'properties', 'geometry', 'image')

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class Group_Perm_Serializer(GroupSerializer):
    permissions = serializers.SerializerMethodField()
    avaible_permissions = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'avaible_permissions')

    def get_permissions(self, obj):
        return list(obj.permissions.values_list('name', flat=True))

    def get_avaible_permissions(self, obj):
        perm = list(obj.permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class User_Perm_Serializer(UserSerializer):
    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups',
                  'user_permissions')

    def get_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def get_user_permissions(self, obj):
        return list(obj.user_permissions.values_list('name', flat=True))

class User_Perm_Admin_Serializer(User_Perm_Serializer):
    avaible_group = serializers.SerializerMethodField()
    avaible_user_permission = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups', 'avaible_group',
                  'user_permissions', 'avaible_user_permission', 'last_login', 'date_joined')

    def get_avaible_group(self, obj):
        perm = list(obj.groups.values_list('name', flat=True))
        return [per for per in Group.objects.all().values_list('name', flat=True)
                if per not in perm]

    def get_avaible_user_permission(self, obj):
        perm = list(obj.user_permissions.values_list('name', flat=True))
        return [per for per in Permission.objects.all().values_list('name', flat=True)
                if per not in perm]

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'password')

    def validate(self, data):
        password = data.get('password')

        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super(UserRegSerializer, self).validate(data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegSerializer, self).update(instance, validated_data)

class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group')
        validators = [
            UniqueTogetherValidator(
                queryset=Dataset.objects.all(),
                fields=['name']
            )
        ]


class DatasetSerializerAdmin(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    avaible_group = serializers.SerializerMethodField()
    properties = serializers.JSONField(required=False, default=[])
    image = serializers.CharField(required=False, default="")
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'type', 'headers', 'properties', 'image', 'group', 'avaible_group')
        validators = [
            UniqueTogetherValidator(
                queryset=Dataset.objects.all(),
                fields=['name']
            )
        ]

    def get_group(self, obj):
        return Group.objects.get(id=obj.group_id).name

    def get_avaible_group(self, obj):
        return [per for per in Group.objects.all().values_list('name', flat=True)
                if (per != Group.objects.get(id=obj.group_id).name)]