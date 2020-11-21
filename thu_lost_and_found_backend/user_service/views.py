import json
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import delete_instance_medias
from thu_lost_and_found_backend.user_service.models import User, UserVerificationApplication, UserInvitation, \
    UserEmailVerification
from thu_lost_and_found_backend.user_service.serializer import UserSerializer, UserVerificationApplicationSerializer, \
    UserInvitationSerializer, UserEmailVerificationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'avatar')
        instance.delete()


class UserVerificationApplicationViewSet(viewsets.ModelViewSet):
    queryset = UserVerificationApplication.objects.all()
    serializer_class = UserVerificationApplicationSerializer


class UserInvitationViewSet(viewsets.ModelViewSet):
    queryset = UserInvitation.objects.all()
    serializer_class = UserInvitationSerializer

    @action(methods=['get', 'post'], url_path=r'register/(?P<token>[\w\d]+)', detail=False)
    def register(self, request, token):
        invitation = get_object_or_404(UserInvitation, token=token)

        if request.method == 'GET':

            invitation_json = json.dumps(UserInvitationSerializer(invitation).data)
            return HttpResponse(invitation_json, content_type='application/json')

        elif request.method == 'POST':
            missing_fields = {}
            contents = json.loads(request.body)
            for field in ["username", "password", "first_name", "last_name"]:
                if field not in contents:
                    missing_fields[field] = ['This field is required.']
            if len(missing_fields) >= 1:
                return HttpResponseBadRequest(json.dumps(missing_fields))

            try:
                new_user = User.objects.create(
                    username=contents['username'],
                    email=invitation.email,
                    password=make_password(contents['password']),
                    first_name=contents['first_name'],
                    last_name=contents['last_name'],
                    is_verified=False,
                    status='ACT',
                    is_staff=True if invitation.role == 'STF' else False,
                    is_superuser=True if invitation.role == 'ADM' else False,
                    date_joined=datetime.now()
                )
            except (IntegrityError, TypeError) as error:
                return HttpResponseBadRequest(error)

            new_user_json = json.dumps(UserSerializer(new_user).data)

            # Remove invitation after creation of user
            invitation.delete()

            return HttpResponse(new_user_json, content_type='application/json')

        else:
            return Http404()


class UserEmailVerificationViewSet(viewsets.ModelViewSet):
    queryset = UserEmailVerification.objects.all()
    serializer_class = UserEmailVerificationSerializer
