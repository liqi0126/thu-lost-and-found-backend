from rest_framework import permissions


class SuperAdminOnlyPermission(permissions.BasePermission):
    message = 'Only Super Admin is allowed.'

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False
