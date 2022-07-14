import json
import sqlite3

from plm import settings

from rest_framework.views import APIView

from rest_framework.parsers import JSONParser, FileUploadParser

from app.models import Feature
from app.serializers import FeatureSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET", "POST", "PUT", "DELETE"])
def TowerAPI(request, id=0):
    if request.method == 'GET':
        feature = Feature.objects.all()
        feature_serializer = FeatureSerializer(feature, many=True)
        return Response(feature_serializer.data)
    elif request.method == 'POST':
        feature_data = JSONParser().parse(request)
        feature_serializer = FeatureSerializer(data=feature_data, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")
    elif request.method == 'PUT':
        feature_data = JSONParser().parse(request)
        feature = Feature.objects.get(id=feature_data['id'])
        feature_serializer = FeatureSerializer(feature, data=feature_data)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success up")
        return Response("Failed up")
    elif request.method == 'DELETE':
        feature = Feature.objects.get(id=id)
        feature.delete()
        return Response("SUCCESS DEL")

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename):
        doc = sqlite3.connect(settings.MEDIA_URL + filename + ".sqlite")
        doc.enable_load_extension(True)

        doc.execute(f'SELECT load_extension("mod_spatialite.dll")')
        cur = doc.cursor()
        cur.execute(f"SELECT *, st_astext(GEOMETRY) from " + filename)
        dict_0 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

        cur.close()

        lis = []
        dict_1 = {}
        dict_1['name'] = filename
        dict_1['type'] = 'Feature'
        dict_1['properties'] = {}
        for value in dict_0:
            for key in value.keys():
                if key == 'geometry' or key == 'id':
                    continue

                if key == 'st_astext(GEOMETRY)':
                    dict_1['geometry'] = value[key]
                    continue

                dict_1['properties'][key] = value[key]
            lis.append(json.dumps(dict_1))

        for i in range(len(lis)):
            lis[i] = json.loads(lis[i])

        feature_serializer = FeatureSerializer(data=lis, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")