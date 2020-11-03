from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from thu_lost_and_found_backend.helpers.toolkits import delete_media_instance
from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.property_service.serializer import PropertyTypeSerializer, PropertyTemplateSerializer, \
    PropertySerializer


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

    def destroy(self, request, pk=None):
        delete_media_instance(PropertyType, pk, 'thumbnail')
        return Response(status=204)


class PropertyTemplateViewSet(viewsets.ModelViewSet):
    queryset = PropertyTemplate.objects.all()
    serializer_class = PropertyTemplateSerializer

    def destroy(self, request, pk=None):
        delete_media_instance(PropertyTemplate, pk, 'thumbnail')
        return Response(status=204)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
