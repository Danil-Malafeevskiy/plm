from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField
from app.models import Feature

'''
class GeometrySerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=100, default="Point")
    class Meta:
        model = Geometry
        fields = ('id', 'type', 'coordinates')


class TowerSerializer(serializers.ModelSerializer):
    name_tap = serializers.CharField(required=False, allow_blank=True, max_length=50, default="")
    VL = serializers.CharField(max_length=100, allow_blank=True, required=False, default="")
    code_support = serializers.CharField(max_length=50, allow_blank=True, required=False, default="Не определен")
    TPV_photo = serializers.CharField(max_length=50, allow_blank=True, required=False, default="")
    UF_photo = serializers.CharField(max_length=50, allow_blank=True, required=False, default="")
    photo = serializers.CharField(max_length=50, allow_blank=True, required=False, default="")
    v_defects = serializers.CharField(max_length=10000, allow_blank=True, required=False, default="")
    u_defects = serializers.CharField(max_length=100, allow_blank=True, required=False, default="")
    code_support_in_1C = serializers.CharField(max_length=200, allow_blank=True, required=False, default="")
    guid = serializers.CharField(max_length=100, allow_blank=True, required=False, default="0")
    flag_defects = serializers.BooleanField(required=False, default=0)
    comment_in_TOiR = serializers.CharField(max_length=100, allow_blank=True, required=False, default="")
    class Meta:
        model = Tower
        fields = ('id', 'name_tap', 'number_support', 'VL', 'type_support', 'code_support', 'material',
                  'corner', 'X', 'Y', 'Z', 'shirota', 'dolgota', 'height',
                  'TPV_photo', 'UF_photo', 'photo', 'v_defects', 'u_defects', 'code_support_in_1C', 'guid', 'flag_defects', 'comment_in_TOiR')
'''


class FeatureSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=100, default="Feature")
    geometry = GeometryField()
    class Meta:
        geo_field = 'geometry'
        model = Feature
        fields = ('id', 'name', 'type', 'properties', 'geometry')

    '''
    def create(self, request):
        geometry_id = request['geometry']
        str_1=''
        if geometry_id['type']=='Point':
            str_1 = f'POINT('+str(geometry_id['coordinates'][0])+' '+str(geometry_id['coordinates'][1])+')'

        feature = Feature.objects.create(type=request['type'], properties=request['properties'], geometry=str_1)

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

        return instance'''