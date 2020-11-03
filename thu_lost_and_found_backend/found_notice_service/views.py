from rest_framework import viewsets

from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.found_notice_service.serializer import FoundNoticeSerializer


class FoundNoticeViewSet(viewsets.ModelViewSet):
    queryset = FoundNotice.objects.all()
    serializer_class = FoundNoticeSerializer
