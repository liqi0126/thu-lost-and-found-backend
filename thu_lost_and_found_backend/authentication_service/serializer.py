from rest_framework import serializers

from thu_lost_and_found_backend.authentication_service.models import UserVerificationApplication


class UserVerificationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerificationApplication
        fields = '__all__'
