from rest_framework import serializers

from thu_lost_and_found_backend.lost_notice_service.models import LostNotice


class LostNoticeSerializer(serializers.ModelSerializer):
    queryset = LostNotice.objects.all()

    class Meta:
        model = LostNotice
        fields = '__all__'
