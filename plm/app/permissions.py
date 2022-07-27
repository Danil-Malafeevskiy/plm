from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return "Can view feature" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'POST':
            return "Can add feature" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'PUT':
            return "Can change feature" in request.user.user_permissions.values_list('name', flat=True)
        if request.method == 'DELETE':
            return "Can delete feature" in request.user.user_permissions.values_list('name', flat=True)

class FileUploadPerm(permissions.BasePermission):
    message = "You don't have enough rights to do this!"

    def has_permission(self, request, view):
        return "Can add feature" in request.user.user_permissions.values_list('name', flat=True)