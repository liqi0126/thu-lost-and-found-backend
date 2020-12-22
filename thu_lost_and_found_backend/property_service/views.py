from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from thu_lost_and_found_backend.helpers.toolkits import delete_instance_medias
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.property_service.serializer import PropertyTypeSerializer, PropertyTemplateSerializer, \
    PropertySerializer

from thu_lost_and_found_backend.matching_service.tasks import update_matching_task


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    filterset_fields = ['name']
    search_fields = ['name']
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'thumbnail')
        instance.delete()


class PropertyTemplateViewSet(viewsets.ModelViewSet):
    queryset = PropertyTemplate.objects.all()
    serializer_class = PropertyTemplateSerializer
    filterset_fields = ['name', 'type__name']
    search_fields = ['name', 'type__name']
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        update_matching_task(self.kwargs['id'])
        serializer.save()

    def perform_destroy(self, instance):
        delete_instance_medias(instance, 'thumbnail')
        instance.delete()


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
