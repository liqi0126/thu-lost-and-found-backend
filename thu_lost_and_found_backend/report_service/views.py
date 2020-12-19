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
    filterset_fields = ['type', 'verdict_type', 'user__username', 'submit_user__username', 'notice_type', 'lost_notice',
                        'found_notice']
    search_fields = ['description', 'user__username', 'submit_user__username', 'verdict']

    # permission_classes = [ReportPermission]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            insert_users_into_request_extra(request)
        except MissingUserField:
            return HttpResponseBadRequest(json.dumps({'user': ['This field is required.']}))

        # There should be no verdict on creation
        request.data.pop('verdict', False)
        request.data.pop('verdict_type', False)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'verdict_type' in request.data:
            # Take down notice if found guilty of charges of report
            if request.data['verdict_type'] == 'GUI':
                if instance.notice_type == 'LST':
                    guilty_notice = instance.lost_notice
                else:
                    guilty_notice = instance.found_notice

                if guilty_notice:
                    instance.lost_notice = None
                    instance.found_notice = None
                    instance.save()
                    guilty_notice.delete()

        # TODO: if notice has been deleted, update other related reports

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
