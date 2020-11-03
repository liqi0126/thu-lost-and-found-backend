from rest_framework import serializers

from thu_lost_and_found_backend.property_service.models import PropertyType


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'
