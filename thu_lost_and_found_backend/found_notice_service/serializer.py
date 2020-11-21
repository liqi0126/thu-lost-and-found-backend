from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.user_service.serializer import UserSerializer


class FoundNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()
    author = UserSerializer(read_only=True)

    # TODO: quizzes

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().create(_property_data)
        # TODO: get auth user
        user = User.objects.get(pk=1)
        found_notice = FoundNotice.objects.create(**validated_data, property=_property, author=user)

        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            found_notice.contacts.add(contact)

        found_notice.save()
        return found_notice

    # TODO: update

    class Meta:
        model = FoundNotice
        fields = '__all__'
