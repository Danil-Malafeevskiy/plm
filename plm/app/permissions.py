from rest_framework import permissions

from app.models import VersionControl

class TowerPerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PUT':
            for group in request.data.keys():
                if f'Изменение объектов {group}' in request.user.user_permissions.values_list('name', flat=True) or group == 'message':
                    continue
                return False
            return True

class FileUploadPerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return f'Изменение объектов {request.data["group"]}' in request.user.user_permissions.values_list('name', flat=True)

class GroupPerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class UserPerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class TypePerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class VersionPerm(permissions.BasePermission):
    message = {'errors': ['Вы не имеете достаточно прав для изменения объектов данной группы!']}

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PUT':
            if request.resolver_match.args[0] == 0:
                return False
            return f'Изменение объектов {VersionControl.objects.get(id=request.resolver_match.args[0]).dataset.name}' \
                   in request.user.user_permissions.values_list('name', flat=True)