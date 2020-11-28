from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSerializer


class LostNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()
    author = UserSerializer(read_only=True)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().create(_property_data)
        # TODO: get auth user
        user = User.objects.get(pk=1)
        lost_notice = LostNotice.objects.create(**validated_data, property=_property, author=user)
        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            lost_notice.contacts.add(contact)
        lost_notice.save()
        return lost_notice

    # TODO: update

    class Meta:
        model = LostNotice
        fields = '__all__'
