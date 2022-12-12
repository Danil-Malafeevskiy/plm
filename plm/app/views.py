import json
import sqlite3

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import transaction, IntegrityError

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FileUploadParser

from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from app.permissions import TowerPerm, FileUploadPerm, GroupPerm, UserPerm, TypePerm, VersionPerm
from plm import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView

from app.models import Feature, Type, VersionControl
from app.serializers import FeatureSerializer, FileSerializer, GroupSerializer, UserSerializer, TypeSerializer, \
    VersionControlSerializer, SetNewPasswordSerializer

from django.core.mail import send_mail

class TowerAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, TowerPerm]
    filterset_fields = ['name']

    def get(self, request, id=0):
        if id == 0:
            groups = list(request.user.groups.values_list('id', flat=True))
            if request.user.is_superuser:
                groups = Group.objects.all()
            datasets = Type.objects.filter(group__in=groups)
            if 'group' in request.query_params:
                datasets = Type.objects.filter(group=Group.objects.get(name=request.query_params['group']).id).values_list('id', flat=True).order_by('id')
            ff = DjangoFilterBackend()

            filtered_queryset = ff.filter_queryset(request, Feature.objects.filter(name__in=list(datasets)), self)

            features = filtered_queryset.extra(
                select={
                    'geometry': 'ST_AsGeoJSON("app_feature"."geometry")'}).values('id', 'name', 'type', 'geometry', 'properties')
            '''for obj in features:
                obj['geometry'] = {"type": GEOSGeometry(obj['geometry']).geom_type, "coordinates": GEOSGeometry(obj['geometry']).coords'''
            return Response(features)
        else:
            feature = Feature.objects.filter(id=id)
            feature_serializer = FeatureSerializer(feature, many=True)
            return Response(feature_serializer.data)

    def put(self, request):
        comment = request.data.pop('message')
        groups_names = []
        conflicts = {}

        try:
            with transaction.atomic():
                for group, groups_data in request.data.items():
                    id_ = []
                    ids = []
                    properties = groups_data.pop(-1)
                    disabled_flexibilities = groups_data.pop(-1)
                    delete_mas = groups_data.pop(-1)

                    for type_name, prop in properties['properties'].items():
                        type = Type.objects.get(name=type_name, group=Group.objects.get(name=group).id)
                        type.properties = prop
                        type.save()

                    for data in groups_data:
                        if 'id' in data.keys():
                            ids.append(data['id'])
                        else:
                            id_.append(data['id_'])

                    ids = ids + delete_mas

                    feature = Feature.objects.filter(id__in=ids)

                    dataset = Group.objects.get(name=group).id
                    groups_names.append(group)

                    feature_serializer = FeatureSerializer(feature, data=groups_data, many=True, context=
                                         {"disabled_flexibilities": disabled_flexibilities, "id_": id_})
                    if feature_serializer.is_valid():
                        version, new_version, conflict = feature_serializer.save()
                        conflicts = dict(list(conflicts.items()) + list(conflict.items()))

                        if VersionControl.objects.filter(flag=True, dataset=dataset).exists():
                            version_now = VersionControl.objects.get(flag=True, dataset=dataset)
                            version_now.flag = False
                            version_now.save()
                            dis_version = VersionControl.objects.filter(
                                date_update__gte=version_now.date_update,
                                dataset=dataset, disabled=False)
                            for vers in dis_version:
                                vers.disabled = True
                                vers.save()

                        OldVersionSerializer = VersionControlSerializer(
                            data={"user": request.user.username, "version": version,
                                  'dataset': dataset, 'comment': comment,
                                  "new_version": new_version})
                        if OldVersionSerializer.is_valid():
                            print(OldVersionSerializer.save())
                    else:
                        raise ValueError(feature_serializer.errors)
                if len(conflicts) > 0:
                    raise IntegrityError
        except ValueError:
            return Response(feature_serializer.errors)
        except IntegrityError:
            return Response(conflicts, status=status.HTTP_409_CONFLICT)

        for group_name in groups_names:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                group_name,
                {
                    'type': 'update.feature',
                    'content': {"groups_names": groups_names}
                }
            )

        return Response("Success up!")

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

        filename = request.data['filename']
        doc.execute(f'SELECT load_extension("mod_spatialite.dll")')

        cur = doc.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        dict_0 = []
        for i in cur.fetchall():
            try:
                cur.execute(f"SELECT *, ST_AsText(GeomFromWKB(GEOMETRY)) from " + i[0])
                dict_0 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
                if dict_0[0]['ST_AsText(GeomFromWKB(GEOMETRY))'] == None:
                    cur.execute(f"SELECT *, ST_AsText(GEOMETRY) from " + i[0])
                    dict_0 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in
                              cur.fetchall()]
                break
            except Exception as e:
                continue

        cur.close()
        doc.close()
        self.fs.delete(request.FILES['file'].name)

        lis = []
        dict_1 = {}
        type = Type.objects.get(name=filename, group=Group.objects.get(name=request.data['group']).id)

        dict_1['name'] = type.id
        dict_1['type'] = 'Feature'
        dict_1['properties'] = {}
        properties = []
        headers = []
        for head in type.headers:
            headers.append(head['text'])

        for prop in type.properties:
            properties.append(prop)

        flag = True
        for value in dict_0:
            for key in value.keys():
                if key == 'GEOMETRY' or key == "geometry" or key == 'id':
                    continue

                if key == 'ST_AsText(GeomFromWKB(GEOMETRY))' or key == 'ST_AsText(GEOMETRY)':
                    dict_1['geometry'] = value[key]
                    continue

                if flag and key not in headers and key not in properties:
                    properties.append(key)

                dict_1['properties'][key] = value[key]
            lis.append(json.dumps(dict_1))

        for i in range(len(lis)):
            lis[i] = json.loads(lis[i])
            lis[i]['geometry'] = {"type": GEOSGeometry(lis[i]['geometry']).geom_type, "coordinates": GEOSGeometry(lis[i]['geometry']).coords}

        return Response({"data": lis, filename: properties, "group": request.data['group']})

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
            group = GroupSerializer(groups, many=True, context=request.user.id, remove_fields=['users'])
            return Response(group.data)

        group = Group.objects.get(id=id)
        groups = GroupSerializer(group, context=request.user.id, remove_fields=['all_user'])
        return Response(groups.data)

    def post(self, request):
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid():
            group = group_serializer.save()

            Permission.objects.create(name=f'Просмотр объектов {group.name}', content_type_id=5, codename=f'view_{group.name}')
            Permission.objects.create(name=f'Изменение объектов {group.name}',
                                      content_type_id=5, codename=f'change_{group.name}')

            for user in request.data['users']:
                get_user_model().objects.get(username=user).groups.add(Group.objects.get(name=request.data['name']))

            if not request.user.is_superuser:
                user = get_user_model().objects.get(id=request.user.id)
                user.groups.add(Group.objects.get(name=group.name))
                user.save()
            return Response("Success new group!")

        return Response({'name': "Группа с таким именем уже существует!"})

    def put(self, request):
        change_group = Group.objects.get(id=request.data['id'])
        group_serializer = GroupSerializer(change_group, data=request.data)
        old_users = GroupSerializer(change_group, remove_fields=['all_user'], context=request.user.id).data['users']

        if group_serializer.is_valid():
            group_serializer.save()
            for user in request.data['users']:
                user_groups = get_user_model().objects.get(username=user).groups
                if request.data['name'] not in user_groups.values_list('name', flat=True):
                    user_groups.add(Group.objects.get(name=request.data['name']))
                else:
                    old_users.remove(user)

            for user in old_users:
                get_user_model().objects.get(username=user).groups.remove(Group.objects.get(name=request.data['name']))
            return Response("Success up group!")
        return Response({'name': "Группа с таким именем уже существует!"})

    def delete(self, request):
        id = request.query_params.get('id')
        groups = Group.objects.filter(id__in= id.split(','))
        for group in groups:
            Permission.objects.get(name=f'Изменение объектов {group.name}').delete()
            Permission.objects.get(name=f'Просмотр объектов {group.name}').delete()
        groups.delete()
        return Response("SUCCESS DEL GROUP!")

class UserView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission']).data)
        if request.user.is_staff:
            return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission']).data)
        return Response(UserSerializer(request.user, remove_fields=['username', 'full_name', 'password', 'avaible_permission',
                                                                    'user_permissions', 'all_users']).data)

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
                                                                                          'image', 'user_permissions', 'all_users'])
            return Response(user_serializer.data)

        return Response(UserSerializer(get_user_model().objects.get(id=id), remove_fields=['username', 'full_name', 'password', 'user_permissions', 'all_users']).data)

    def post(self, request):
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
            if request.user.is_superuser:
                datasets = ff.filter_queryset(request, Type.objects.all(), self)
            if 'group' in request.query_params:
                datasets = Type.objects.filter(group=Group.objects.get(name=request.query_params['group']).id)
            dataset = ff.filter_queryset(request, datasets, self)
            return Response(TypeSerializer(dataset, many=True, remove_fields=['type', 'headers',
                                                                                 'properties', 'image', 'group_type', 'all_group_type']).data)

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
                                                                                 'properties', 'image', 'group_type', 'all_group_type']).data)

        dataset = Type.objects.get(id=id)
        return Response(TypeSerializer(dataset).data)

    def post(self, request):
        dataset_serializer = TypeSerializer(data=request.data, context={'group': request.data['group'], 'ruls': request.data['ruls']})
        if dataset_serializer.is_valid():
            dataset_serializer.save()
            return Response("Success new dataset!")
        return Response(dataset_serializer.errors)

    def put(self, request):
        dataset = Type.objects.get(id=request.data['id'])
        dataset_serializer = TypeSerializer(dataset, data=request.data, context={'group': request.data['group'], 'ruls': request.data['ruls']})
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
            if request.user.is_superuser:
                datasets = Group.objects.all()
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
                date_update__gte=version.date_update, date_update__lt=version_now[0].date_update, disabled=False).order_by('-id')
            version.flag = True
            version.save()

        elif len(version_now)!=0 and (version_now[0].date_update <= version.date_update):
            if 'flag' in request.data.keys():
                all_version = VersionControl.objects.filter(
                    dataset=versionSer['dataset'],
                    date_update__gte=version_now[0].date_update, date_update__lte=dateformat.format(timezone.now(), 'Y-m-d H:i:s'), disabled=False).order_by('id')
            else:
                all_version = VersionControl.objects.filter(
                    dataset=versionSer['dataset'],
                    date_update__gte=version_now[0].date_update, date_update__lt=version.date_update, disabled=False).order_by('id')

                version.flag = True
                version.save()

            flag = True

        else:
            all_version = VersionControl.objects.filter(
                dataset=versionSer['dataset'],
                date_update__gte=version.date_update, date_update__lte=dateformat.format(timezone.now(), 'Y-m-d H:i:s'), disabled=False).order_by('-id')
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