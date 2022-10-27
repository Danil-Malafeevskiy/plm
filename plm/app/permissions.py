from rest_framework import permissions

class TowerPerm(permissions.BasePermission):
    message = "Вы не имеете достаточно прав для изменения объектов данной группы!"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PUT':
            return f'Изменение объектов {request.data.pop(-1)}' in request.user.user_permissions.values_list('name', flat=True)

class FileUploadPerm(permissions.BasePermission):
    message = "Вы не имеете достаточно прав для изменения объектов данной группы!"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return f'Изменение объектов {request.data["group"]}' in request.user.user_permissions.values_list('name', flat=True)

class GroupPerm(permissions.BasePermission):
    message = "У вас нет прав для данного действия!"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class UserPerm(permissions.BasePermission):
    message = "У вас нет прав для данного действия!"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class TypePerm(permissions.BasePermission):
    message = "У вас нет прав для данного действия!"

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

class VersionPerm(permissions.BasePermission):
    message = "Вы не имеете достаточно прав для изменения объектов данной группы!"

    def has_permission(self, request, view):
        print(view.id)
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return "Can view version control" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return "Can change version control" in request.user.user_permissions.values_list('name', flat=True)