from rest_framework import viewsets

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.lost_notice_service.serializer import LostNoticeSerializer


class LostNoticeViewSet(viewsets.ModelViewSet):
    queryset = LostNotice.objects.all()
    serializer_class = LostNoticeSerializer
