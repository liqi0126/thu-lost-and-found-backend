from rest_framework import viewsets
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MatchingEntry, MatchingHyperParam
from .serializer import MatchingEntrySerializer, MatchingHyperParamSerializer
from .tasks import update_matching_task
from .notify import matching_notify


class MatchingHyperParamViewSet(viewsets.ModelViewSet):
    queryset = MatchingHyperParam.objects.all()
    serializer_class = MatchingHyperParamSerializer

    @action(detail=False, methods=['get'], url_path=r'get-hyper')
    def get_hyper(self, request):
        instance = MatchingHyperParam.get_hyper()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path=r'update-hyper')
    def update_hyper(self, request):
        instance = MatchingHyperParam.get_hyper()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        update_matching_task.delay()
        return Response(serializer.data)


class MatchingEntryViewSet(viewsets.ModelViewSet):
    queryset = MatchingEntry.objects.all()
    serializer_class = MatchingEntrySerializer
    pagination_class = LimitOffsetPagination
    ordering = ['matching_degree']
    filter_fields = ['lost_notice_id', 'found_notice_id']

    @action(detail=True, methods=['post'], url_path='matching-notify')
    def matching_notify(self, request, pk):
        matching_entry = MatchingEntry.objects.get(pk=pk)
        matching_entry.notified = False
        matching_notify(matching_entry)
        return Response("ok")
