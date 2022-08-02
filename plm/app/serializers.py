import json

from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from app.models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=100, default="Feature")
    geometry = GeometryField()
    class Meta:
        geo_field = 'geometry'
        model = Feature
        fields = ('id', 'name', 'type', 'properties', 'geometry', 'group')

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')

class Group_Perm_Serializer(serializers.ModelSerializer):
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

    def create(self, request):
        new_group = Group.objects.create(name=request['name'])
        return new_group

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'