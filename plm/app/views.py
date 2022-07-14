import json
import sqlite3
from plm import settings

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework import viewsets, response
import geojson


from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from django.http.response import JsonResponse
from rest_framework.viewsets import ModelViewSet

from app.models import Feature
from app.serializers import FeatureSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, schema



@api_view(["GET", "POST", "PUT", "DELETE"])
def TowerAPI(request, id=0):
    if request.method == 'GET':
        feature = Feature.objects.all()
        feature_serializer = FeatureSerializer(feature, many=True, )
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
        feature = Feature.objects.all()
        feature.delete()
        return Response("SUCCESS DEL")

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename):
        doc = sqlite3.connect(settings.MEDIA_URL + filename + ".sqlite")
        cur = doc.cursor()

        cur.execute("SELECT ST_ASTEXT(ST_GeogFromWKB(GEOMETRY)) from " + filename)
        #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

        print(cur.fetchall())
        return Response(cur.fetchall())
        lis = []
        dict_1 = {}
        for i in doc_1['features']:
            dict_1['name']=doc_1['name']
            dict_1['type']=i['type']
            dict_1['properties'] = i['properties']
            dict_1['geometry'] = i['geometry']
            lis.append(json.dumps(dict_1))

        for i in range(len(doc_1['features'])):
            lis[i] = json.loads(lis[i])

        feature_serializer = FeatureSerializer(data=lis, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")