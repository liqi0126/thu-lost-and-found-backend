import json

from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.contact_service.serializer import ContactSimpleSerializer
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice, FoundNoticeStatus
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.property_service.serializer import PropertySerializer
from thu_lost_and_found_backend.user_service.models import User
from thu_lost_and_found_backend.matching_service.models import MatchingEntry
from thu_lost_and_found_backend.matching_service.serializer import MatchingEntrySerializer

from thu_lost_and_found_backend.helpers.match import matching
from thu_lost_and_found_backend.user_service.serializer import UserSimpleSerializer


class FoundNoticeSerializer(serializers.ModelSerializer):
    contacts = ContactSimpleSerializer(many=True)
    property = PropertySerializer()
    author = UserSimpleSerializer(read_only=True)
    matching_entries = MatchingEntrySerializer(many=True, read_only=True)

    # TODO: quizzes

    def create(self, validated_data):
        author_id = json.loads(validated_data.pop('extra'))['author']
        contacts_data = validated_data.pop('contacts')
        _property_data = validated_data.pop('property')
        _property = PropertySerializer().create(_property_data)
        author = User.objects.get(pk=author_id)
        found_notice = FoundNotice.objects.create(**validated_data, property=_property, author=author)

        # TODO: threading
        # matching
        lost_notices = LostNotice.objects.filter(status=FoundNoticeStatus.OPEN, property__template=found_notice.property.template)
        for lost_notice in lost_notices:
            matching_degree = matching(lost_notice, found_notice)
            matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice, matching_degree=matching_degree)
            matching_entry.save()

        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            found_notice.contacts.add(contact)

        found_notice.save()

        # matching
        lost_notices = LostNotice.objects.filter(status=FoundNoticeStatus.OPEN,
                                                 property__template=found_notice.property.template)
        for lost_notice in lost_notices:
            matching_degree = matching(lost_notice, found_notice)
            matching_entry = MatchingEntry.objects.create(lost_notice=lost_notice, found_notice=found_notice,
                                                          matching_degree=matching_degree)
            matching_entry.save()

        return found_notice

    # def update(self, instance, validated_data):
    #     print(instance)
    #     contacts_data = validated_data.pop('contacts')
    #     _property_data = validated_data.pop('property')
    #
    #     for contact_data in contacts_data:
    #         pass

    class Meta:
        model = FoundNotice
        fields = '__all__'
