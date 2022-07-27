import json
import os
import sqlite3

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from app.permissions import IsOwner, FileUploadPerm
from plm import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser

from app.models import Feature
from app.serializers import FeatureSerializer, FileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes


@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated, IsOwner])
def TowerAPI(request, id=0):
    if request.method == 'GET':
        feature = Feature.objects.filter(group=request.user.groups.values_list('id', flat=True).first())
        feature_serializer = FeatureSerializer(feature, many=True)
        return Response(feature_serializer.data)
    elif request.method == 'POST':
        for obj in request.data:
            obj['group'] = request.user.groups.values_list('id', flat=True).first()
        feature_serializer = FeatureSerializer(data=request.data, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")
    elif request.method == 'PUT':
        feature = Feature.objects.get(id=request.data['id'], group=request.user.groups.values_list('id', flat=True).first())
        feature_serializer = FeatureSerializer(feature, data=request.data)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success up")
        return Response("Failed up")
    elif request.method == 'DELETE':
        try:
           feature = Feature.objects.get(id=id, group=request.user.groups.values_list('id', flat=True).first())
        except Exception:
            return Response("There is no access to this object!")
        feature.delete()
        return Response("SUCCESS DEL")

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    serializer_class = FileSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, FileUploadPerm]

    fs = FileSystemStorage(location=settings.MEDIA_URL)

    def put(self, request):
        self.fs.save(request.FILES['file'].name, request.FILES['file'])
        doc = sqlite3.connect(settings.MEDIA_URL + request.FILES['file'].name)
        doc.enable_load_extension(True)

        filename, res = os.path.splitext(self.request.FILES['file'].name)

        doc.execute(f'SELECT load_extension("mod_spatialite.dll")')
        cur = doc.cursor()
        cur.execute(f"SELECT *, st_astext(GEOMETRY) from " + filename)
        dict_0 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

        cur.close()
        doc.close()
        self.fs.delete(request.FILES['file'].name)

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
            dict_1['group'] = request.user.groups.values_list('id', flat=True).first()
            lis.append(json.dumps(dict_1))

        for i in range(len(lis)):
            lis[i] = json.loads(lis[i])

        feature_serializer = FeatureSerializer(data=lis, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")

class LoginView(APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response("Success login")
            else:
                return Response("Failed login")
        else:
            return Response("Failed login")

class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response("Success logout")

class GroupView(APIView):

    def get(self, request):
        group = Group.objects.all()
        return Response(group.values_list('name', flat=True))

    def post(self, request):
        new_group, created = Group.objects.get_or_create(name=request.data['name'])
        return Response("suc")

