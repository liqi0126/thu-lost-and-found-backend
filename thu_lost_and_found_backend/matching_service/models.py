from django.db import models
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice

# Create your models here.


class MatchingEntry(models.Model):
    lost_notice = models.ForeignKey(LostNotice, on_delete=models.CASCADE, related_name='matching_entries')
    found_notice = models.ForeignKey(FoundNotice, on_delete=models.CASCADE, related_name='matching_entries')
    matching_degree = models.FloatField(default=0.)
