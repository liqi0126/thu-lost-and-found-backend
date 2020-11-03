from rest_framework import serializers

from thu_lost_and_found_backend.found_notice_service.models import FoundNotice


class FoundNoticeSerializer(serializers.ModelSerializer):
    queryset = FoundNotice.objects.all()

    class Meta:
        model = FoundNotice
        fields = '__all__'
