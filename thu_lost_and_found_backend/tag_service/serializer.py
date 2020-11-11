from rest_framework import serializers

from thu_lost_and_found_backend.tag_service.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
