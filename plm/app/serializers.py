from rest_framework import serializers, authentication
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
