from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from app.models import Tower
from app.serializers import TowerSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET", "POST", "PUT", "DELETE"])
def TowerAPI(request, id=0):
    if request.method == 'GET':
        tower = Tower.objects.all()
        tower_serializer = TowerSerializer(tower, many=True)
        return Response(tower_serializer.data)
    elif request.method == 'POST':
        tower_data = JSONParser().parse(request)
        tower_serializer = TowerSerializer(data=tower_data)
        if tower_serializer.is_valid():
            tower_serializer.save()
            return Response("Success new")
        return Response("Failed new")
    elif request.method == 'PUT':
        tower_data = JSONParser().parse(request)
        tower = Tower.objects.get(id=tower_data['number_support'])
        tower_serializer = TowerSerializer(tower, data=tower_data)
        if tower_serializer.is_valid():
            tower_serializer.save()
            return Response("Success up")
        return JsonResponse("Failed up", safe=False)
    elif request.method == 'DELETE':
        tower = Tower.objects.get(Unique_number=id)
        tower.delete()
        return Response("SUCCESS DEL")

