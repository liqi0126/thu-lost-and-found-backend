from rest_framework import serializers

from .models import MatchingEntry, MatchingHyperParam


class MatchingHyperParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingHyperParam
        fields = '__all__'


class MatchingEntrySerializer(serializers.ModelSerializer):
    lost_notice_images = serializers.JSONField(source='lost_notice.images')
    lost_notice_description = serializers.CharField(source='lost_notice.description')
    lost_property_name = serializers.CharField(source='lost_notice.property.name')
    found_notice_images = serializers.JSONField(source='found_notice.images')
    found_notice_description = serializers.CharField(source='found_notice.description')
    found_property_name = serializers.CharField(source='found_notice.property.name')

    class Meta:
        model = MatchingEntry
        fields = '__all__'
