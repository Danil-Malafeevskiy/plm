from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from app.models import Tower
from app.serializers import TowerSerializer

@csrf_exempt
def TowerAPI(request, id=0):
    if request.method == 'GET':
        tower = Tower.objects.all()
        tower_serializer = TowerSerializer(tower, many=True)
        return JsonResponse(tower_serializer.data, safe=False)
    elif request.method == 'POST':
        tower_data = JSONParser().parse(request)
        tower_serializer = TowerSerializer(data=tower_data)
        if tower_serializer.is_valid():
            tower_serializer.save()
            return JsonResponse("Success new", safe=False)
        return JsonResponse("Failed new", safe=False)
    elif request.method == 'PUT':
        tower_data = JSONParser().parse(request)
        tower = Tower.objects.get(id=tower_data['number_support'])
        tower_serializer = TowerSerializer(tower, data=tower_data)
        if tower_serializer.is_valid():
            tower_serializer.save()
            return JsonResponse("Success up", safe=False)
        return JsonResponse("Failed up", safe=False)
    elif request.method == 'DELETE':
        tower = Tower.objects.get(Unique_number=id)
        tower.delete()
        return JsonResponse("SUCCESS DEL", safe=False)