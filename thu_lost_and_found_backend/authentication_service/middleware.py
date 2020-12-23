from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from rest_framework_simplejwt import authentication


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


class UserStatusValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            if user.status == 'INA':
                data = {
                    'message': 'Your account is Inactive. Please contact system admin for activation.'
                }
                return JsonResponse(status=403, data=data)
            elif user.status == 'SUS':
                data = {
                    'message': 'Your account is suspended due to user reports or illicit behaviours.',
                }
                return JsonResponse(status=403, data=data)

        response = self.get_response(request)
        return response
