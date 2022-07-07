from rest_framework import serializers
from app.models import Tower, Geometry, Feature

class GeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Geometry
        fields = ('id', 'type', 'coordinates')


class TowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tower
        fields = ('id', 'name_tap', 'number_support', 'VL', 'type_support', 'code_support', 'material',
                  'corner', 'X', 'Y', 'Z', 'shirota', 'dolgota', 'height',
                  'TPV_photo', 'UF_photo', 'photo', 'v_defects', 'u_defects', 'code_support_in_1C', 'guid', 'flag_defects', 'comment_in_TOiR')

class FeatureSerializer(serializers.ModelSerializer):
    properties = TowerSerializer(required=True)
    geometry = GeometrySerializer(required=True)

    class Meta:
        model = Feature
        fields = ('id', 'properties', 'geometry')

    def create(self, request):
        geometry_id = request['geometry']
        tower_id = request['properties']
        properties = TowerSerializer.create(TowerSerializer(), validated_data=tower_id)
        geometry = GeometrySerializer.create(GeometrySerializer(), validated_data=geometry_id)

        feature = Feature.objects.create(type=request['type'], properties=properties, geometry=geometry)

        return feature

    def update(self, instance, request):
        geometry_id = request['geometry']
        tower_id = request['properties']
        properties = TowerSerializer.update(self, instance=instance.properties, validated_data=tower_id)
        geometry = GeometrySerializer.update(self, instance=instance.geometry, validated_data=geometry_id)

        instance.type = request['type']
        instance.properties = properties
        instance.geometry = geometry
        instance.save()

        return instance