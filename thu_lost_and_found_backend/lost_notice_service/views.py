from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from thu_lost_and_found_backend.helpers.toolkits import save_uploaded_image
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.lost_notice_service.serializer import LostNoticeSerializer


class LostNoticeViewSet(viewsets.ModelViewSet):
    queryset = LostNotice.objects.all()
    serializer_class = LostNoticeSerializer

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        notice = get_object_or_404(LostNotice, pk=pk)
        image_path = save_uploaded_image(request, 'lost_notice_images', notice)
        # If save failed
        if not image_path:
            return HttpResponseBadRequest()
        # Update database
        notice.images['images'].append(image_path)
        notice.save()

        return HttpResponse('Upload success.')
