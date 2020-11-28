from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from thu_lost_and_found_backend.helpers.toolkits import delete_instance_medias
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.property_service.serializer import PropertyTypeSerializer, PropertyTemplateSerializer, \
    PropertySerializer


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'thumbnail')
        instance.delete()


class PropertyTemplateViewSet(viewsets.ModelViewSet):
    queryset = PropertyTemplate.objects.all()
    serializer_class = PropertyTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'thumbnail')
        instance.delete()


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
