from rest_framework import viewsets
from rest_framework.pagination import CursorPagination


from .models import MatchingEntry
from .serializer import MatchingEntrySerializer


class MatchingEntryViewSet(viewsets.ModelViewSet):
    queryset = MatchingEntry.objects.all()
    serializer_class = MatchingEntrySerializer
    pagination_class = CursorPagination
    ordering = ['matching_degree']
    filter_fields = ['lost_notice_id', 'found_notice_id']
