import json

from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.matching_service.serializer import MatchingEntrySerializer
from thu_lost_and_found_backend.user_service.serializer import UserSimpleSerializer


from .tasks import create_matching_task, update_matching_task


class FoundNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()
    author = UserSimpleSerializer(read_only=True)
    matching_entries = MatchingEntrySerializer(many=True, read_only=True)


    def create(self, validated_data):
        author_id = json.loads(validated_data.pop('extra'))['author']
        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().create(_property_data)
        author = User.objects.get(pk=author_id)
        found_notice = FoundNotice.objects.create(**validated_data, property=_property, author=author)

        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            found_notice.contacts.add(contact)
        found_notice.save()

        create_matching_task.delay(found_notice.id)

        return found_notice

    def update(self, instance, validated_data):
        author_id = json.loads(validated_data.pop('extra'))['author']

        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().update(instance.property, _property_data)

        found_notice = serializers.ModelSerializer.update(self, instance, validated_data)
        found_notice.author = User.objects.get(id=author_id)

        # clean old notices
        for contact in found_notice.contacts.all():
            if contact.found_notices.count() == 1:
                contact.delete()
        found_notice.contacts.clear()

        # add new contacts
        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            found_notice.contacts.add(contact)
        found_notice.save()

        update_matching_task.delay(found_notice.id)

        return found_notice

    class Meta:
        model = FoundNotice
        fields = '__all__'
