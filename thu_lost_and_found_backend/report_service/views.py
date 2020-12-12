import json

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import check_missing_fields
from thu_lost_and_found_backend.report_service.models import Report
from thu_lost_and_found_backend.report_service.serializer import ReportSerializer
from thu_lost_and_found_backend.user_service.models import User


class MissingUserField(Exception):
    pass


def insert_users_into_request_extra(request):
    missing_fields = check_missing_fields(request.data, ["user"])
    if missing_fields:
        raise MissingUserField

    report_user = get_object_or_404(User, pk=request.data['user'])

    request.data['extra'] = json.dumps(
        {
            'user': report_user.id,
            'submit_user': request.user.id
        }
    )


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            insert_users_into_request_extra(request)
        except MissingUserField:
            return HttpResponseBadRequest(json.dumps({'user': ['This field is required.']}))

        # There should be no verdict on creation
        request.data['verdict'] = None

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
