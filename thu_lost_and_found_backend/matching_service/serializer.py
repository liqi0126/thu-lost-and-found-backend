from rest_framework import serializers

from .models import MatchingEntry

class MatchingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingEntry
        fields = '__all__'
