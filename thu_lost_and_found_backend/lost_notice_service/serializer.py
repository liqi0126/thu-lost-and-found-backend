from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.models import Property
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer


class LostNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().create(_property_data)

        lost_notice = LostNotice.objects.create(**validated_data, property=_property)
        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            lost_notice.contacts.add(contact)
        lost_notice.save()
        return lost_notice

    # TODO: update

    class Meta:
        model = LostNotice
        fields = '__all__'
