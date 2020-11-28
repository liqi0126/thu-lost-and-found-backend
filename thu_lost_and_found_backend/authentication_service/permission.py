from rest_framework import permissions


class SuperAdminOnlyPermission(permissions.BasePermission):
    message = 'Only Super Admin is allowed.'

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False


class AdminOnlyExceptUserMeActionPermission(permissions.BasePermission):
    message = 'Only Admin is allowed except /user/me/ .'

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if request.path == 'user/me/':
                return True
            return user.is_staff

        return False
