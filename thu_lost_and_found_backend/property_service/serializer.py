from rest_framework import serializers

from thu_lost_and_found_backend.property_service.models import PropertyType, PropertyTemplate, Property
from thu_lost_and_found_backend.tag_service.models import Tag
from thu_lost_and_found_backend.tag_service.serializer import TagSimpleSerializer


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
    template_queryset = PropertyTemplate.objects.all()
    template = serializers.PrimaryKeyRelatedField(queryset=template_queryset)
    tags = TagSimpleSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        _property = Property.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            _property.tags.add(tag)
        _property.save()
        return _property

    # TODO: update

    class Meta:
        model = Property
        fields = '__all__'
