from rest_framework import viewsets

from .models import MatchingEntry
from .serializer import MatchingEntrySerializer


class MatchingEntryViewSet(viewsets.ModelViewSet):
    queryset = MatchingEntry.objects.all()
    serializer_class = MatchingEntrySerializer
