from rest_framework import permissions

class TowerPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view feature" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT':
            return "Can change feature" in request.user.user_permissions.values_list('name', flat=True)

class FileUploadPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        return "Can add feature" in request.user.user_permissions.values_list('name', flat=True)

class GroupPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view group" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return "Can change group" in request.user.user_permissions.values_list('name', flat=True)

class UserPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view user" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return "Can change user" in request.user.user_permissions.values_list('name', flat=True)

class DatasetPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view dataset" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return "Can change dataset" in request.user.user_permissions.values_list('name', flat=True)

class VersionPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view version control" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return "Can change version control" in request.user.user_permissions.values_list('name', flat=True)