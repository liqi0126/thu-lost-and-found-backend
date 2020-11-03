from rest_framework import serializers

from thu_lost_and_found_backend.contact_service.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
