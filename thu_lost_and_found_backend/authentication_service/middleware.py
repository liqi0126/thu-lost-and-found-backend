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
