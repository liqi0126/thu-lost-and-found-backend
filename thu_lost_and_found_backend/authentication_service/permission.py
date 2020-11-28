import re
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from thu_lost_and_found_backend.user_service.models import User


class SuperAdminOnlyPermission(permissions.BasePermission):
    message = 'Only Super Admin is allowed.'

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False


class UserPermission(permissions.BasePermission):
    message = 'Only authenticated user can access its user.'

    def has_permission(self, request, view):
        user = request.user
        path = request.path

        if user and user.is_authenticated:
            if request.path == '/users/me/':
                return True
            else:
                crud_user_match = re.match(string=path, pattern=r'^/users/(\d+)/')
                crud_user_id = crud_user_match.group(1) if crud_user_match else None
                crud_user = get_object_or_404(User, pk=crud_user_id)

                if crud_user != user and not user.is_staff:
                    return False
                else:
                    return True

        return False
