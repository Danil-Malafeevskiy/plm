import json
import os
import sqlite3

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FileUploadParser

from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from app.permissions import TowerPerm, FileUploadPerm, GroupPerm, UserPerm, TypePerm, VersionPerm
from plm import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView

from app.models import Feature, Type, VersionControl
from app.serializers import FeatureSerializer, FileSerializer, GroupSerializer, UserSerializer, TypeSerializer, \
    VersionControlSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from django.core.mail import send_mail

class TowerAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, TowerPerm]
    filterset_fields = ['name']

    def get(self, request, id=0):
        if id == 0:
            datasets = Type.objects.filter(group__in=list(request.user.groups.values_list('id', flat=True)))
            if 'group' in request.query_params:
                datasets = Type.objects.filter(group=Group.objects.get(name=request.query_params['group']).id)
            ff = DjangoFilterBackend()
            filtered_queryset = ff.filter_queryset(request, Feature.objects.filter(name__in=
                list(datasets.values_list('id', flat=True))).order_by('id'), self)

            feature_serializer = FeatureSerializer(filtered_queryset, many=True, remove_fields=['image'])
            return Response(feature_serializer.data)
        else:
            feature = Feature.objects.filter(id=id)
            feature_serializer = FeatureSerializer(feature, many=True)
            return Response(feature_serializer.data)

    def put(self, request):
        ids = []
        queryset = []
        comment = request.data.pop(-1)
        delete_mas = request.data.pop(-1)
        if len(delete_mas)!=0:
            queryset = Feature.objects.extra(where=["geometrytype(geometry) LIKE 'LINESTRING'"]).filter(
                name__in=Type.objects.filter(group=Feature.objects.get(id=delete_mas[0]).name.group.id))
        for data in request.data:
            if 'id' in data.keys():
                if data['geometry']['type'] == "Point" and len(queryset)==0:
                    queryset = Feature.objects.extra(where=["geometrytype(geometry) LIKE 'LINESTRING'"]).filter(name__in=Type.objects.filter(group=Feature.objects.get(id=data['id']).name.group.id))
                ids.append(data['id'])

        ids = ids + delete_mas

        feature = Feature.objects.filter(id__in=ids)

        if len(ids)==0:
            dataset = Type.objects.get(id=request.data[0]['name']).group.id
            group_name = Type.objects.get(id=request.data[0]['name']).group.name
        else:
            dataset = feature[0].name.group.id
            group_name = feature[0].name.group.name

        feature_serializer = FeatureSerializer(feature, data=request.data, many=True, context=FeatureSerializer(queryset, many=True).data)
        if feature_serializer.is_valid():
            version, new_version = feature_serializer.save()
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                group_name,
                {
                    'type': 'update.feature',
                    'content': 'Все объекты добавлены и обновлены!'
                }
            )
            try:
                VersionControl.objects.filter(date_update__gte=VersionControl.objects.get(flag=True, dataset=dataset).date_update, dataset=dataset).delete()
            except Exception as e:
                print("Ваша версия максимальна!")

            OldVersionSerializer = VersionControlSerializer(
                data={"user": request.user.username, "version": version,
                      'dataset': dataset, 'comment': comment,
                      "new_version": new_version})
            if OldVersionSerializer.is_valid():
                OldVersionSerializer.save()
            else:
                return Response(OldVersionSerializer.errors)
            return Response("Success up!")

        return Response(feature_serializer.errors)

class FileUploadView(APIView):

    serializer_class = FileSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, FileUploadPerm]
    parser_classes = (MultiPartParser, FileUploadParser,)

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
        try:
            type = Type.objects.get(name=filename, group=Group.objects.get(name=request.data['group']).id)
        except Exception:
            return Response({"error": "Создайте тип такой же как имя файла!"})
        dict_1['name'] = type.id
        dict_1['type'] = 'Feature'
        dict_1['properties'] = {}
        properties = []
        headers = []
        for obj in type.headers:
            headers.append(obj['text'])
        flag = True
        for value in dict_0:
            if len(properties)!=0:
                flag=False
            for key in value.keys():
                if key == 'geometry' or key == 'id':
                    continue

                if key == 'st_astext(GEOMETRY)':
                    dict_1['geometry'] = value[key]
                    continue

                if flag and key not in headers:
                    properties.append(key)

                dict_1['properties'][key] = value[key]
            lis.append(json.dumps(dict_1))

        type.properties = properties
        type.save()

        for i in range(len(lis)):
            lis[i] = json.loads(lis[i])

        feature_serializer = FeatureSerializer(data=lis, many=True, context=False)
        if feature_serializer.is_valid():
            feature_serializer.save()
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                request.data['group'],
                {
                    'type': 'update.feature',
                    'content': 'Все объекты добавлены!'
                }
            )
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
                return Response({"error": "Пользователь не активный"})
        else:
            return Response({"error": "Такого пользователя не найдено. Проверьте данные входа."})

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response("Success logout")

class GroupView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [GroupPerm]

    def get(self, request, id=0):
        if id==0:
            if request.user.is_superuser:
                groups = Group.objects.all()
            else:
                groups_list = [group for group in list(request.user.groups.values_list('name', flat=True))
                                                                    if group != "Admin"]
                groups = Group.objects.filter(name__in=groups_list)
            group = GroupSerializer(groups, many=True, context=request.user.id)
            return Response(group.data)

        group = Group.objects.get(id=id)
        groups = GroupSerializer(group, remove_fields=['all_user'])
        return Response(groups.data)

    def post(self, request):
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid():
            group = group_serializer.save()

            if not request.user.is_superuser:
                user = get_user_model().objects.get(id=request.user.id)
                user.groups.add(Group.objects.get(name=group.name))
                user.save()
            return Response("Success new group!")

        return Response({group_serializer.errors['name']: "Группа с таким именем уже существует!"})

    def put(self, request):
        change_group = Group.objects.get(id=request.data['id'])
        group_serializer = GroupSerializer(change_group, data=request.data)
        if group_serializer.is_valid():
            group_serializer.save()
            return Response("Success up group!")
        return Response({group_serializer.errors['name']: "Группа с таким именем уже существует!"})

    def delete(self, request):
        id = request.query_params.get('id')
        Group.objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL GROUP!")

class UserView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission']).data)
        if request.user.is_staff:
            return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission', 'admin_permissions']).data)
        return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission',
                                                                    'admin_permissions', 'user_permissions']).data)

class UserAdminView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [UserPerm]
    filterset_fields = ['username', 'is_staff', 'groups']

    def get(self, request, id=0):
        if id == 0:
            ff = DjangoFilterBackend()
            users = get_user_model().objects.filter(groups__name__in=[group for group in list(request.user.groups.values_list('name', flat=True))
                                                                    if group != "Admin"]).distinct().exclude(id=request.user.id)

            if request.user.is_superuser:
                users = get_user_model().objects.all().exclude(id=request.user.id)

            filtered_queryset = ff.filter_queryset(request, users, self)


            user_serializer = UserSerializer(filtered_queryset, many=True, remove_fields=['username', 'password', 'first_name', 'last_name',
                                                                                          'is_superuser', 'is_staff',
                                                                                          'groups',
                                                                                          'permissions',
                                                                                          'avaible_permission',
                                                                                          'image', 'admin_permissions', 'user_permissions'])
            return Response(user_serializer.data)

        return Response(UserSerializer(get_user_model().objects.get(id=id), remove_fields=['username', 'full_name', 'password', 'is_superuser', 'is_staff', 'admin_permissions', 'user_permissions']).data)

    def post(self, request):
        if "Admin" in request.data['groups']:
            request.data['is_staff'] = True

        request.data['password'] = get_user_model().objects.make_random_password(length=16)
        request.data['username'] = request.data['email']

        reg = UserSerializer(data=request.data, context={'permissions': request.data['permissions'], 'groups': request.data['groups']})
        if reg.is_valid():
            try:
                send_mail('Пароль для входа на сайт', f'Ваш пароль: {request.data["password"]}',
                      settings.DEFAULT_FROM_EMAIL, [request.data['email']])
            except Exception:
                return Response({"error": "Неккоректный email."})
            reg.save()
            return Response({"id": reg.data['id']})
        return Response({"email": "Такой email уже зарегистрирован!"})

    def put(self, request):
        user = get_user_model().objects.get(id=request.data['id'])
        if 'password' in request.data.keys():
            user_serializer = UserSerializer(user, data=request.data)
        else:
            user_serializer = UserSerializer(user, data=request.data, remove_fields=['password'],
                                             context={'permissions': request.data['permissions'],
                                                      'groups': request.data['groups']})

        if user_serializer.is_valid():
            if 'password' in request.data.keys():
                send_mail('Пароль для входа на сайт изменен', f'Ваш новый пароль: {request.data["password"]}',
                          settings.DEFAULT_FROM_EMAIL, [request.data["email"]])

            if request.data['email'] != user.email:
                try:
                    send_mail('Смена почты', 'Ваша почта была изменена на эту!',
                              settings.DEFAULT_FROM_EMAIL, [request.data["email"]])
                except Exception:
                    return Response({'email': ["Введенная почта некорректна!"]})

            user_serializer.save()
            return Response("Success up!")
        return Response(user_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        get_user_model().objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL USER!")

class TypeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type']

    def get(self, request, id=0):
        if id==0:
            ff = DjangoFilterBackend()
            datasets = Type.objects.filter(group__in=list(request.user.groups.values_list('id', flat=True)))
            if 'group' in request.query_params:
                datasets = Type.objects.filter(group=Group.objects.get(name=request.query_params['group']).id)
            dataset = ff.filter_queryset(request, datasets, self)
            return Response(TypeSerializer(dataset, many=True, remove_fields=['type', 'headers',
                                                                                 'properties', 'image', 'group']).data)

        dataset = Type.objects.get(id=id)
        return Response(TypeSerializer(dataset).data)

class TypeAdminView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [TypePerm]
    filterset_fields = ['type']

    def get(self, request, id=0):
        if id==0:
            ff = DjangoFilterBackend()
            datasets = ff.filter_queryset(request, Type.objects.filter(group__in=list(request.user.groups.values_list('id', flat=True))), self)
            if request.user.is_superuser:
                datasets = ff.filter_queryset(request, Type.objects.all(), self)
            if 'group' in request.query_params:
                datasets = Type.objects.filter(group=Group.objects.get(name=request.query_params['group']).id)
            return Response(TypeSerializer(datasets, many=True, remove_fields=['type', 'headers',
                                                                                 'properties', 'image']).data)

        dataset = Type.objects.get(id=id)
        return Response(TypeSerializer(dataset).data)

    def post(self, request):
        dataset_serializer = TypeSerializer(data=request.data, context={'group': request.data['group']})
        if dataset_serializer.is_valid():
            dataset_serializer.save()
            return Response("Success new dataset!")
        return Response(dataset_serializer.errors)

    def put(self, request):
        dataset = Type.objects.get(id=request.data['id'])
        dataset_serializer = TypeSerializer(dataset, data=request.data, context={'group': request.data['group']})
        if dataset_serializer.is_valid():
            dataset_serializer.save()
            return Response("Success update dataset!")
        return Response(dataset_serializer.errors)

    def delete(self, request):
        id = request.query_params.get('id')
        Type.objects.filter(id__in=id.split(',')).delete()
        return Response("SUCCESS DEL")

class VersionControlView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [VersionPerm]
    filterset_fields = ['user']

    def get(self, request, id=0):
        if id==0:
            ff = DjangoFilterBackend()
            datasets = list(request.user.groups.values_list('id', flat=True))
            if 'dataset' in request.query_params:
                datasets = [Group.objects.filter(name=request.query_params['dataset'])[0].id]
            version = ff.filter_queryset(request, VersionControl.objects.filter(dataset__in=datasets).order_by('id'), self)
            return Response(VersionControlSerializer(version, many=True, remove_fields=['version', 'new_version', 'dataset']).data)

        version = VersionControl.objects.get(id=id)
        return Response(VersionControlSerializer(version, remove_fields=['dataset']).data)


    def put(self, request, id=0):
        version = VersionControl.objects.get(id=id)
        versionSer = VersionControlSerializer(version).data
        version_now = VersionControl.objects.filter(flag=True, dataset=versionSer['dataset'])
        flag = False

        if len(version_now)!=0:
            version_now[0].flag = False
            version_now[0].save()

        if (len(version_now)!=0 and version_now[0].date_update > version.date_update):
            all_version = VersionControl.objects.filter(
                dataset=versionSer['dataset'],
                date_update__gte=version.date_update, date_update__lt=version_now[0].date_update).order_by('-id')
            version.flag = True
            version.save()

        elif len(version_now)!=0 and (version_now[0].date_update <= version.date_update):
            if 'flag' in request.data.keys():
                all_version = VersionControl.objects.filter(
                    dataset=versionSer['dataset'],
                    date_update__gte=version_now[0].date_update, date_update__lte=dateformat.format(timezone.now(), 'Y-m-d H:i:s')).order_by('id')
            else:
                all_version = VersionControl.objects.filter(
                    dataset=versionSer['dataset'],
                    date_update__gte=version_now[0].date_update, date_update__lt=version.date_update).order_by('id')

                version.flag = True
                version.save()

            flag = True

        else:
            all_version = VersionControl.objects.filter(
                dataset=versionSer['dataset'],
                date_update__gte=version.date_update, date_update__lte=dateformat.format(timezone.now(), 'Y-m-d H:i:s')).order_by('-id')
            version.flag = True
            version.save()

        errors = []
        for i in range(len(all_version)):
            mas_versions = []
            ids = []
            if flag == False:
                del_param = all_version[i].version['delete']
                up_param = all_version[i].version['update']
                create_param = all_version[i].version['create']
            else:
                del_param = all_version[i].new_version['delete']
                up_param = all_version[i].new_version['update']
                create_param = all_version[i].new_version['create']

            mas_versions += (create_param + up_param)
            for obj_2 in up_param:
                if obj_2['id'] not in ids:
                    ids.append(obj_2['id'])
            for obj_2 in del_param:
                if obj_2 not in ids:
                    ids.append(obj_2)

            feature_serializer = FeatureSerializer(Feature.objects.filter(id__in=ids), data=mas_versions, many=True, context=False)

            if feature_serializer.is_valid():
                feature_serializer.save()
            else:
                errors.append(feature_serializer.errors)
        if len(errors)==0:
            return Response("Version Return!")
        return Response(errors)

class RequestResetPassword(APIView):
    def post(self, request):
        if get_user_model().objects.filter(email=request.data['email']).exists():
            user = get_user_model().objects.get(email=request.data['email'])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Перейдите по ссылке для изменения пароля:'
            send_mail('Сброс и изменение пароля', f'{email_body} \n{absurl}',
                      settings.DEFAULT_FROM_EMAIL, [request.data["email"]])
            return Response({'success': "Ссылка на изменение пароля отправлена на ваш Email!"})
        return Response("Мы не можем найти предоставленный Email. Проверьте введенные данные.")

class ResetPassword(APIView):

    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'success': False})

        return Response({'success': True, 'uidb64': uidb64, 'token': token})

class SetNewPassword(APIView):
    def put(self, request):
        pass_serializer = SetNewPasswordSerializer(data=request.data)
        if pass_serializer.is_valid():
            return Response("Пароль успешно изменен!")
        return Response(pass_serializer.errors)