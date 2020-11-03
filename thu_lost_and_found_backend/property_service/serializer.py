from rest_framework import serializers

from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property


class PropertyTemplateSerializer(serializers.ModelSerializer):
    queryset = PropertyType.objects.all()
    type = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = PropertyTemplate
        fields = ['id', 'type', 'name', 'thumbnail', 'fields']


class PropertyTypeSerializer(serializers.ModelSerializer):
    templates = PropertyTemplateSerializer(many=True, read_only=True)

    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'thumbnail', 'templates']


class PropertySerializer(serializers.ModelSerializer):
    queryset = PropertyTemplate.objects.all()
    template = serializers.PrimaryKeyRelatedField(queryset=queryset)

    # TODO: add notices
    class Meta:
        model = Property
        fields = '__all__'
