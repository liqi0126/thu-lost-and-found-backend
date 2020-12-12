import json

from rest_framework import serializers

from thu_lost_and_found_backend.report_service.models import Report
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSimpleSerializer


class ReportSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    submit_user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        extra = json.loads(validated_data.pop('extra'))
        report_user_id = extra['user']
        submit_user_id = extra['submit_user']

        report_user = User.objects.get(pk=report_user_id)
        submit_user = User.objects.get(pk=submit_user_id)

        report = Report.objects.create(**validated_data, user=report_user, submit_user=submit_user)

        return report
