from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from app.models import Feature, Tower, Geometry
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
        tower = Tower.objects.get(id=id)
        geometry = Geometry.objects.get(id=id)
        tower.delete()
        geometry.delete()
        return Response("SUCCESS DEL")

