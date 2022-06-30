from rest_framework import serializers
from app.models import Tower


class TowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tower
        fields = ('id', 'Unique_number', 'name_tap', 'number_support', 'VL', 'type_support', 'code_support', 'material',
                  'corner', 'X', 'Y', 'Z', 'shirota', 'dolgota', 'height',
                  'TPV_photo', 'UF_photo', 'photo', 'v_defects', 'u_defects', 'code_support_in_1C', 'guid', 'flag_defects', 'comment_in_TOiR', 'geometry')