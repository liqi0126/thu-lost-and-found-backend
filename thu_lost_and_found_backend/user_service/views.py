import json

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

        if request.method == 'GET':
            invitation = get_object_or_404(UserInvitation, token=token)
            invitation_json = json.dumps(UserInvitationSerializer(invitation).data)
            return HttpResponse(invitation_json, content_type='application/json')

        elif request.method == 'POST':
            missing_fields = {}
            for field in ["username", "password", "nickname", "document_number", "mobile", "email"]:
                if field not in request.POST:
                    missing_fields[field] = ['This field is required.']
            if len(missing_fields) >= 1:
                return HttpResponseBadRequest(json.dumps(missing_fields))
        else:
            return Http404()


class UserEmailVerificationViewSet(viewsets.ModelViewSet):
    queryset = UserEmailVerification.objects.all()
    serializer_class = UserEmailVerificationSerializer
