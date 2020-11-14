from rest_framework import viewsets

from thu_lost_and_found_backend.tag_service.models import Tag
from thu_lost_and_found_backend.tag_service.serializer import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
