import json

from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import save_uploaded_images, delete_instance_medias
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.lost_notice_service.serializer import LostNoticeSerializer


class LostNoticeViewSet(viewsets.ModelViewSet):
    queryset = LostNotice.objects.all()
    serializer_class = LostNoticeSerializer
    pagination_class = CursorPagination
    ordering = ['-updated_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    # TODO: Custom property type, templates, author filter
    filterset_fields = ['description', 'status', 'est_lost_start_datetime', 'est_lost_end_datetime', 'lost_location',
                        'reward']
    search_fields = ['description', 'status', 'est_lost_start_datetime', 'est_lost_end_datetime', 'lost_location',
                     'reward']

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if len(request.FILES) != 0:
            images_url = save_uploaded_images(request, 'lost_notice_images', model=LostNotice)
            request.data['images'] = json.dumps({"images_url": images_url})
            # Update serializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'images', json=True)
        instance.delete()

    # TODO: update json images

    @action(detail=True, methods=['post'], url_path='upload-image/')
    def upload_image(self, request):
        result = save_uploaded_images(request, 'lost_notice_images', LostNotice)
        if result:
            return JsonResponse(result, safe=False)
        else:
            return HttpResponseBadRequest()
