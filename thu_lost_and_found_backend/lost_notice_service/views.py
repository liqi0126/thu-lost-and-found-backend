import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from thu_lost_and_found_backend.helpers.toolkits import save_uploaded_images
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.lost_notice_service.serializer import LostNoticeSerializer


class LostNoticeViewSet(viewsets.ModelViewSet):
    queryset = LostNotice.objects.all()
    serializer_class = LostNoticeSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if len(request.FILES) != 0:
            images_url = save_uploaded_images(request, 'lost_notice_images', model=LostNotice)
            request.data['images'] = json.dumps(images_url)
            # Update serializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        notice = get_object_or_404(LostNotice, pk=pk)

        if save_uploaded_images(request, 'lost_notice_images', notice):
            return HttpResponse('Upload success.')
        else:
            return HttpResponseBadRequest()
