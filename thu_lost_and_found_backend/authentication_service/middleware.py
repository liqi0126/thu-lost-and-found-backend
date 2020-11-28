import re

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt import authentication
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is not authenticated with django auth system
        # Check its JWT
        if not request.user.is_authenticated:
            request.user = authentication.JWTAuthentication().authenticate(request)
            request.user = request.user[0] if request.user else AnonymousUser()

        response = self.get_response(request)
        return response


class NoticesAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        user = request.user

        if request.method not in permissions.SAFE_METHODS:
            lost_notice_match = re.match(string=path, pattern=r'^/lost-notices/(\d+)/')
            lost_notice_id = lost_notice_match.group(1) if lost_notice_match else None

            found_notice_match = re.match(string=path, pattern=r'^/found-notices/(\d+)/')
            found_notice_id = found_notice_match.group(1) if found_notice_match else None

            if lost_notice_match or found_notice_match:
                if lost_notice_id:
                    author = get_object_or_404(LostNotice, pk=lost_notice_id).author
                else:
                    author = get_object_or_404(FoundNotice, pk=found_notice_id).author

                # Reject if user is not author or staff
                if author != user and not user.is_staff:
                    return HttpResponseForbidden()

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
