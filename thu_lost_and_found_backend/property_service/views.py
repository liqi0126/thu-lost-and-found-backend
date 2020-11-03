from rest_framework import viewsets

from thu_lost_and_found_backend.property_service.models import PropertyType
from thu_lost_and_found_backend.property_service.serializer import PropertyTypeSerializer


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

