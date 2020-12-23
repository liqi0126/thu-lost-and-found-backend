import re

from django.shortcuts import get_object_or_404
from rest_framework import permissions

from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice


class SuperAdminOnlyPermission(permissions.BasePermission):
    message = 'Only Super Admin is allowed.'

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False


class NoticePermission(permissions.BasePermission):
    message = 'Notice permission denied'

    def has_permission(self, request, view):
        path = request.path
        user = request.user

        # Check if is owner's notice
        # Can't use .check_object_permissions(request, obj) as its method is custom
        if request.method not in permissions.SAFE_METHODS:

            if not user.is_authenticated:
                return False

            lost_notice_match = re.match(string=path, pattern=r'^/api/v1/lost-notices/(\d+)/')
            lost_notice_id = lost_notice_match.group(1) if lost_notice_match else None

            found_notice_match = re.match(string=path, pattern=r'^/api/v1/found-notices/(\d+)/')
            found_notice_id = found_notice_match.group(1) if found_notice_match else None

            author = None
            if lost_notice_id:
                author = get_object_or_404(LostNotice, pk=lost_notice_id).author
            elif found_notice_id:
                author = get_object_or_404(FoundNotice, pk=found_notice_id).author

            # Reject if user is not author or staff
            if author != user and not user.is_staff:
                return False

        # If GET request
        else:
            # Only staff can filter list status, else status = PUB
            if re.match(string=path, pattern=r'^/api/v1/(lost|found)-notices/$'):
                request.GET._mutable = True
                if not user.is_staff:
                    # User can filter own posts by status
                    if 'author__id' in request.GET and user:
                        if int(request.GET['author__id']) == user.id:
                            return True

                    request.GET['status'] = 'PUB'

        return True


class UserPermission(permissions.BasePermission):
    message = 'Only authenticated user can access its user.'

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        path = request.path

        if re.match(string=path, pattern=r'^/api/v1/users/(\d+)/simple-info/$'):
            return True

        if user != obj and not user.is_staff:
            return False
        return True


class ReportPermission(permissions.BasePermission):
    message = 'User can only create or view reports.'

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            # Normal user can only create but not edit
            if request.method != 'POST':
                if not user.is_staff:
                    return False

        return True
