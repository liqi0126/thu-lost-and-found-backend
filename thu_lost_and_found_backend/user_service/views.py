import json
import re
from datetime import datetime, timedelta

import requests
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from thu_lost_and_found_backend import settings
from thu_lost_and_found_backend.helpers.toolkits import save_uploaded_images, delete_media_from_url
from thu_lost_and_found_backend.authentication_service.permission import SuperAdminOnlyPermission, UserPermission
from thu_lost_and_found_backend.helpers.toolkits import delete_instance_medias, check_missing_fields, random_string
from thu_lost_and_found_backend.matching_service.match import MatchingHyperParam
from thu_lost_and_found_backend.matching_service.models import MatchingEntry
from thu_lost_and_found_backend.matching_service.serializer import MatchingEntrySerializer
from thu_lost_and_found_backend.matching_service.views import MatchingEntryViewSet
from thu_lost_and_found_backend.user_service.models import User, UserVerificationApplication, UserInvitation, \
    UserEmailVerification, UserStatus
from thu_lost_and_found_backend.user_service.serializer import UserSerializer, UserVerificationApplicationSerializer, \
    UserInvitationSerializer, UserEmailVerificationSerializer, UserSimpleSerializer
from .email_verification_template import email_verification_template
from .invitation_template import invitation_template


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['first_name', 'last_name', 'username',
                        'student_id', 'status', 'is_staff', 'is_superuser', 'is_active', 'is_verified']

    search_fields = ['first_name', 'last_name', 'username', 'student_id', 'status']
    permission_classes = [UserPermission]

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'avatar')
        instance.delete()

    @action(methods=['get'], url_path=r'me', detail=False)
    def current_user_info(self, request):
        user_json = json.dumps(UserSerializer(request.user).data)
        return HttpResponse(user_json, content_type='application/json')

    @action(methods=['get'], url_path=r'simple-info', detail=True)
    def simple_info(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_json = json.dumps(UserSimpleSerializer(user).data)
        return HttpResponse(user_json, content_type='application/json')

    @action(detail=True, methods=['get'], url_path=r'get-high-matching-entry')
    def get_high_matching_entry(self, request, pk):
        queryset = MatchingEntry.objects.filter(lost_notice__author=pk, matching_degree__gt=MatchingHyperParam.get_matching_threshold())
        page = MatchingEntryViewSet.paginate_queryset(self, queryset=queryset)
        if page is not None:
            serializer = MatchingEntrySerializer(page, many=True)
            return MatchingEntryViewSet.get_paginated_response(self, serializer.data)

        serializer = MatchingEntrySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path=r'wechat_thu_auth')
    def wechat_auth(self, request, pk):
        url = "https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token"
        reply = requests.post(url, {"token": request.data.get('token', '')})

        if reply.status_code == 200:
            reply = reply.json()
            user = User.objects.get(pk=pk)
            user.is_verified = True
            user.student_id = reply['user']['card']
            user.department = reply['user']['department']
            user.save()

        return Response(reply)

    @action(methods=['get'], url_path=r'statistic', detail=False)
    def statistic(self, request):
        return Response({
            'total': User.objects.count(),
            'active': User.objects.filter(status=UserStatus.ACTIVE).count(),
            'inactive': User.objects.filter(status=UserStatus.INACTIVE).count(),
            'suspended': User.objects.filter(status=UserStatus.SUSPENDED).count(),
            'verified': User.objects.filter(is_verified=True).count(),
            'staff': User.objects.filter(is_staff=True).count()
        })

    @action(detail=False, methods=['post'], url_path=r'upload-avatar')
    def upload_avatar(self, request):
        if 'id' in request.data:
            instance_id = request.data['id']
        else:
            id_max = User.objects.all().aggregate(Max('id'))['id__max']
            instance_id = id_max + 1 if id_max else 1

        result = save_uploaded_images(request, 'user_avatars', instance_id=instance_id)
        if result:
            return Response({'url': result})
        else:
            return HttpResponseBadRequest()

    @action(detail=False, methods=['post'], url_path=r'delete-avatar')
    def delete_avatar(self, request):
        if 'url' in request.data:
            image_url = request.data['url']
        else:
            return HttpResponseBadRequest('url is required.')

        try:
            delete_media_from_url(image_url)
            return Response('Image deleted')
        except (ValueError, OSError) as error:
            return HttpResponseBadRequest(error)


class UserVerificationApplicationViewSet(viewsets.ModelViewSet):
    queryset = UserVerificationApplication.objects.all()
    serializer_class = UserVerificationApplicationSerializer
    filterset_fields = ['status', 'user__username']
    search_fields = ['status', 'user__username', 'description']
    permission_classes = [IsAdminUser]


class UserInvitationViewSet(viewsets.ModelViewSet):
    queryset = UserInvitation.objects.all()
    serializer_class = UserInvitationSerializer

    permission_classes = []

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['token'] = random_string(64)
        # if 'expiration_date' not in request.data:
        request.data['expiration_date'] = make_aware(datetime.now() + timedelta(weeks=2))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if user with that email exists
        try:
            User.objects.get(email=request.data['email'])
            return HttpResponseBadRequest(f'User with this "{request.data["email"]}" email already exists.')
        except User.DoesNotExist:
            pass

        self.perform_create(serializer)

        send_mail(subject='THU Lost-and-Found Invitation Link',
                  message='',
                  html_message=invitation_template.format(
                      role=request.data['role'],
                      invitation_link=f'{settings.APP_URL}/#/invitation/{request.data["token"]}/',
                      expiration_date=request.data['expiration_date'].strftime('%d-%m-%Y')
                  ),

                  from_email=f'"{settings.EMAIL_DISPLAY_NAME}" <{settings.EMAIL_HOST_USER}>',
                  recipient_list=[request.data['email']],
                  fail_silently=False)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get', 'post'], url_path=r'register/(?P<token>[\w\d]+)', detail=False)
    def register(self, request, token):
        invitation = get_object_or_404(UserInvitation, token=token)

        if invitation.expiration_date <= timezone.now():
            invitation.delete()
            return Http404()

        if request.method == 'GET':
            invitation_json = json.dumps(UserInvitationSerializer(invitation).data)
            return HttpResponse(invitation_json, content_type='application/json')

        elif request.method == 'POST':
            contents = json.loads(request.body)
            missing_fields = check_missing_fields(contents, ["username", "password", "first_name", "last_name"])
            if missing_fields:
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
                    is_staff=True if invitation.role == 'STF' or invitation.role == 'ADM' else False,
                    is_superuser=True if invitation.role == 'ADM' else False,
                    date_joined=make_aware(datetime.now())
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

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        request.data['token'] = random_string(64)
        if 'expiration_date' not in request.data:
            request.data['expiration_date'] = make_aware(datetime.now() + timedelta(weeks=2))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if user is already verified
        user = request.user

        if user.is_verified:
            return HttpResponseBadRequest(f'User "{user.username}" has already been verified.')
        # Check if valid email
        if not re.match(string=request.data['email'], pattern=r'.+@mails?\.tsinghua\.edu\.cn$'):
            return HttpResponseBadRequest('Email must be Tsinghua\'s email.')

        self.perform_create(serializer)

        send_mail(subject='THU Lost-and-Found Email Verification Link',
                  message='',
                  html_message=email_verification_template.format(
                      username=user.username,
                      verification_link=f'{settings.APP_URL}/#/email-verification/{request.data["token"]}/',
                      expiration_date=request.data['expiration_date'].strftime('%d-%m-%Y')
                  ),
                  from_email=f'"{settings.EMAIL_DISPLAY_NAME}" <{settings.EMAIL_HOST_USER}>',
                  recipient_list=[request.data['email']],
                  fail_silently=False)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], url_path=r'verify/(?P<token>[\w\d]+)', detail=False)
    def verify_user(self, request, token):
        verification_entry = get_object_or_404(UserEmailVerification, token=token)

        if verification_entry.expiration_date <= timezone.now():
            verification_entry.delete()
            return Http404()

        username = verification_entry.user.username
        verification_entry.user.is_verified = True
        verification_entry.user.save()
        # Remove verification_entry after verification of user
        verification_entry.delete()

        return HttpResponseRedirect(f'{settings.APP_URL}/#/verified/{username}/')
