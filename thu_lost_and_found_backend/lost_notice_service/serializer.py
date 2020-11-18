from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer


class LostNoticeSerializer(serializers.ModelSerializer):
    queryset = LostNotice.objects.all()
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        lost_notice = LostNotice.objects.create(**validated_data)
        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            lost_notice.contacts.add(contact)
        lost_notice.save()
        return lost_notice

    # TODO: update

    class Meta:
        model = LostNotice
        fields = '__all__'
