import json
import os
import sqlite3

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Func, CharField

from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from app.permissions import IsOwner, FileUploadPerm
from plm import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser
from app.models import Feature, Dataset
from app.serializers import FeatureSerializer, FileSerializer, GroupSerializer, UserSerializer, DatasetSerializer
from rest_framework.response import Response

class GeometryType(Func):
    function = "GeometryType"
    output_field = CharField()

class TowerAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ['name']
    serializer_class = FeatureSerializer

    def get(self, request, id=0):
        if id == 0:
            ff = DjangoFilterBackend()
            filtered_queryset = ff.filter_queryset(request, Feature.objects.filter(name__in=
                list(Dataset.objects.filter(group__in=list(request.user.groups.values_list('id', flat=True))).values_list('id', flat=True))), self)

            feature_serializer = FeatureSerializer(filtered_queryset, many=True, remove_fields=['image'])
            return Response(feature_serializer.data)
        else:
            feature = Feature.objects.filter(id=id)
            feature_serializer = FeatureSerializer(feature, many=True)
            return Response(feature_serializer.data)

    def post(self, request):
        feature_serializer = FeatureSerializer(data=request.data, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success new qqq")
        return Response(feature_serializer.errors)

    def put(self, request):
        feature = Feature.objects.filter(id__in=request.query_params.get('id').split(','))
        print(list(feature))
        feature_serializer = FeatureSerializer(feature, data=request.data, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
            return Response("Success up")
        return Response(feature_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        Feature.objects.filter(id__in=id.split(',')).delete()
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
        dict_1['name'] = Dataset.objects.get(name=filename).id
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
        return Response(feature_serializer.errors)

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
                return Response("A user not active.")
        else:
            return Response("A user with this username and password is not found.")

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
            group = GroupSerializer(groups, many=True, remove_fields=['permissions', 'avaible_permissions'])
            return Response(group.data)

        group = Group.objects.get(id=id)
        groups = GroupSerializer(group)
        return Response(groups.data)

    def options(self, request, *args, **kwargs):
        return Response(Permission.objects.all().values_list('name', flat=True))

    def post(self, request):
        group_serializer = GroupSerializer(data=request.data, context={'permissions': request.data['permissions']})
        if group_serializer.is_valid():
            group_serializer.save()
            return Response("Success new group!")

        return Response(group_serializer.errors)

    def put(self, request):
        change_group = Group.objects.get(id=request.data['id'])
        group_serializer = GroupSerializer(change_group, data=request.data, context={'permissions': request.data['permissions']})
        if group_serializer.is_valid():
            group_serializer.save()
            return Response("Success up group!")
        return Response(group_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        Group.objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL GROUP!")

class UserView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user, remove_fields=['password']).data)

class UserAdminView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    filterset_fields = ['username', 'is_staff', 'groups']

    def get(self, request, id=0):
        if id == 0:
            ff = DjangoFilterBackend()
            filtered_queryset = ff.filter_queryset(request, User.objects.all(), self)


            user_serializer = UserSerializer(filtered_queryset, many=True, remove_fields=['password', 'first_name', 'last_name', 'email',
                                                                                          'is_superuser', 'is_staff', 'is_active',
                                                                                          'groups', 'avaible_group',
                                                                                          'permissions',
                                                                                          'avaible_permission',
                                                                                          'last_login', 'date_joined'])
            return Response(user_serializer.data)

        user_serializer = UserSerializer(User.objects.get(id=id), remove_fields=['password'])
        return Response(user_serializer.data)

    def post(self, request):
        reg = UserSerializer(data=request.data, context={'permissions': request.data['permissions'], 'groups': request.data['groups']})
        if reg.is_valid():
            reg.save()
            return Response({"id": reg.data['id']})
        return Response(reg.errors)

    def put(self, request):
        user = User.objects.get(id=request.data['id'])
        if 'password' in request.data.keys():
            user_serializer = UserSerializer(user, data=request.data)
        else:
            user_serializer = UserSerializer(user, data=request.data, remove_fields=['password'],
                                             context={'permissions': request.data['permissions'],
                                                      'groups': request.data['groups']})

        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Success up!")
        return Response(user_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        User.objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL USER!")

class DatasetView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type']

    def get(self, request, id=0):
        if id==0:
            ff = DjangoFilterBackend()
            dataset = ff.filter_queryset(request, Dataset.objects.filter(group__in=list(request.user.groups.values_list('id', flat=True))), self)
            return Response(DatasetSerializer(dataset, many=True, remove_fields=['type', 'headers',
                                                                                 'properties', 'image', 'group', 'avaible_group']).data)

        dataset = Dataset.objects.get(id=id)
        return Response(DatasetSerializer(dataset, remove_fields=['group', 'avaible_group']).data)

class DatasetAdminView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    filterset_fields = ['type']

    def get(self, request, id=0):
        if id==0:
            ff = DjangoFilterBackend()
            dataset = ff.filter_queryset(request, Dataset.objects.all(), self)
            return Response(DatasetSerializer(dataset, many=True, remove_fields=['type', 'headers',
                                                                                 'properties', 'image', 'group', 'avaible_group']).data)

        dataset = Dataset.objects.get(id=id)
        return Response(DatasetSerializer(dataset).data)

    def post(self, request):
        dataset_serializer = DatasetSerializer(data=request.data, context={'group': request.data['group']})
        if dataset_serializer.is_valid():
            dataset_serializer.save()
            return Response("Success new dataset!")
        return Response(dataset_serializer.errors)

    def put(self, request):
        dataset = Dataset.objects.get(id=request.data['id'])
        dataset_serializer = DatasetSerializer(dataset, data=request.data, context={'group': request.data['group']})
        if dataset_serializer.is_valid():
            dataset_serializer.save()
            return Response("Success update dataset!")
        return Response(dataset_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        Dataset.objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL")

def room(request):
    return render(request, 'E:/KT/plm/plm/templates/test.html')