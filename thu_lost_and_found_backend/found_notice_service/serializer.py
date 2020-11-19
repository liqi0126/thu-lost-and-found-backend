from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer


class FoundNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer(read_only=True)

    # TODO: quizzes

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        lost_notice = FoundNotice.objects.create(**validated_data)
        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            lost_notice.contacts.add(contact)
        lost_notice.save()
        return lost_notice

    # TODO: update

    class Meta:
        model = FoundNotice
        fields = '__all__'
