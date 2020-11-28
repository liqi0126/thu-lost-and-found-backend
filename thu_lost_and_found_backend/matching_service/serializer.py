from rest_framework import serializers

from .models import MatchingEntry


class MatchingEntrySerializer(serializers.ModelSerializer):
    lost_notice_images = serializers.CharField(source='lost_notice.images')
    lost_notice_description = serializers.CharField(source='lost_notice.description')
    found_notice_images = serializers.CharField(source='found_notice.images')
    found_notice_description = serializers.CharField(source='found_notice.description')
    class Meta:
        model = MatchingEntry
        fields = '__all__'
