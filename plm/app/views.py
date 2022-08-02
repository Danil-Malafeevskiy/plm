import json
import os
import sqlite3

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission, User
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.permissions import IsOwner, FileUploadPerm
from plm import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser

from app.models import Feature
from app.serializers import FeatureSerializer, FileSerializer, GroupSerializer, Group_Perm_Serializer, UserSerializer
from rest_framework.response import Response

class TowerAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, id=0):
        if id == 0:
            feature = Feature.objects.filter(group=request.user.groups.values_list('id', flat=True).first())
        else:
            feature = Feature.objects.filter(id=id, group=request.user.groups.values_list('id', flat=True).first())
        feature_serializer = FeatureSerializer(feature, many=True)
        return Response(feature_serializer.data)

    def post(self, request):
        for obj in request.data:
            obj['group'] = request.user.groups.values_list('id', flat=True).first()
        feature_serializer = FeatureSerializer(data=request.data, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new")
        return Response("Failed new")

    def put(self, request):
        feature = Feature.objects.get(id=request.data['id'], group=request.user.groups.values_list('id', flat=True).first())
        feature_serializer = FeatureSerializer(feature, data=request.data)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success up")
        return Response("Failed up")

    def delete(self, request, id):
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
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response("Success logout")

class GroupView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, id=0):
        if id==0:
            groups = Group.objects.all()
            group = GroupSerializer(groups, many=True)
            return Response(group.data)

        group = Group.objects.get(id=id)
        groups = Group_Perm_Serializer(group)
        return Response(groups.data)

    def options(self, request, *args, **kwargs):
        return Response(Permission.objects.all().values_list('name', flat=True))

    def post(self, request):
        group_serializer = Group_Perm_Serializer(data=request.data)
        if group_serializer.is_valid():
            new_group = group_serializer.save()
            for perm in request.data['permissions']:
                new_group.permissions.add(Permission.objects.get(name=perm))
            return Response("Success new!")
        return Response("The selected name already exists!")

    def put(self, request):
        change_group = Group.objects.get(id=request.data['id'])
        group_serializer = Group_Perm_Serializer(change_group, data=request.data)
        if group_serializer.is_valid():
            change_group = group_serializer.save()
            change_group.permissions.clear()
            for perm in request.data['permissions']:
                change_group.permissions.add(Permission.objects.get(name=perm))
            return Response("Success up group!")
        return Response("The selected name already exists!")

    def delete(self, request, id):
        Group.objects.get(id=id).delete()
        return Response("SUCCESS DEL GROUP!")

class UserView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)