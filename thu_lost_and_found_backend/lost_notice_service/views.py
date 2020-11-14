from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from thu_lost_and_found_backend.helpers.toolkits import save_uploaded_images
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.lost_notice_service.serializer import LostNoticeSerializer


class LostNoticeViewSet(viewsets.ModelViewSet):
    queryset = LostNotice.objects.all()
    serializer_class = LostNoticeSerializer

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        notice = get_object_or_404(LostNotice, pk=pk)
        image_url = save_uploaded_images(request, 'lost_notice_images', notice)
        # If save failed
        if not image_url:
            return HttpResponseBadRequest()
        # Update database
        if not notice.images:
            notice_images = {'image_urls': []}
        else:
            notice_images = notice.images

        notice_images['image_urls'].extend(image_url)
        notice.images = notice_images
        notice.save()

        return HttpResponse('Upload success.')
