from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.serializer import ContactSerializer
from thu_lost_and_found_backend.user_service.models import User, UserVerificationApplication, UserInvitation, \
    UserEmailVerification


class UserSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    contacts = ContactSerializer(many=True, read_only=True)
    found_notice = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    found_lost_property_notices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lost_notice = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    returned_lost_property_notices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    verification_application = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'wechat_openid', 'extra', 'created_at', 'updated_at']


class UserSimpleSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'wechat_avatar', 'avatar', 'is_verified', 'status']


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
