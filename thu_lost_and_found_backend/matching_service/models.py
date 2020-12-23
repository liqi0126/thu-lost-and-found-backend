from django.db import models
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.found_notice_service.models import FoundNotice

# Create your models here.


class MatchingHyperParam(models.Model):
    matching_threshold = models.FloatField(default=0.5)

    notice_location_weight = models.FloatField(default=2)
    notice_time_weight = models.FloatField(default=2)
    notice_desc_weight = models.FloatField(default=0.5)
    notice_extra_weight = models.FloatField(default=1.)

    prop_tag_weight = models.FloatField(default=1.)
    prop_desc_weight = models.FloatField(default=0.5)
    prop_extra_weight = models.FloatField(default=1)

    extra = models.JSONField(null=True)

    @staticmethod
    def get_hyper():
        if MatchingHyperParam.objects.count() == 0:
            instance = MatchingHyperParam.objects.create()
            instance.save()
        return MatchingHyperParam.objects.get(pk=1)

    @staticmethod
    def get_matching_threshold():
        instance = MatchingHyperParam.get_hyper()
        return instance.matching_threshold


class MatchingEntry(models.Model):
    lost_notice = models.ForeignKey(LostNotice, on_delete=models.CASCADE, related_name='matching_entries')
    found_notice = models.ForeignKey(FoundNotice, on_delete=models.CASCADE, related_name='matching_entries')
    matching_degree = models.FloatField(default=0.)
    notified = models.BooleanField(default=False)
