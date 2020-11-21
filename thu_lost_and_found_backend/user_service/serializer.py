from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.serializer import ContactSerializer
from thu_lost_and_found_backend.user_service.models import User, UserVerificationApplication, UserInvitation, \
    UserEmailVerification


class UserSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'wechat_id', 'avatar', 'date_joined', 'contacts']


class UserVerificationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerificationApplication
        fields = '__all__'


class UserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvitation
        fields = '__all__'


class UserEmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailVerification
        fields = '__all__'
