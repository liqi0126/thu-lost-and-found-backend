from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.serializer import ContactSerializer
from thu_lost_and_found_backend.user_service.models import User


class UserSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'wechat_id', 'avatar', 'date_joined', 'contacts']
