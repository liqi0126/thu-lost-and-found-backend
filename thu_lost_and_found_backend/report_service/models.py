from django.db import models
from django.utils.translation import gettext_lazy as _

from thu_lost_and_found_backend.found_notice_service.models import FoundNotice
from thu_lost_and_found_backend.lost_notice_service.models import LostNotice
from thu_lost_and_found_backend.user_service.models import User


class ReportType(models.TextChoices):
    SCAM = 'SCM', _('Scam')
    HARASSMENT = "HRS", _('Harassment')
    ADVERTISEMENT = 'ADV', _('Advertisement')
    PORN = 'PRN', _('Porn')
    ILLEGAL_CONTENT = 'ILL', _('Illegal Content')
    SPAM = 'SPM', _('Spam')
    COPYRIGHT_VIOLATION = 'CPY', _('Copyright Violation')
    OTHERS = 'OTH', _('Others')


class NoticeType(models.TextChoices):
    LOST = 'LST', _('Lost')
    FOUND = "FND", _('Found')


class VerdictType(models.TextChoices):
    GUILTY = 'GUI', _('Guilty')
    INNOCENCE = "INN", _('Innocence')
    UNTREATED = "UNT", _('Untreated')


class Report(models.Model):
    type = models.CharField(max_length=3, choices=ReportType.choices, default=ReportType.SCAM)
    description = models.CharField(max_length=500, null=True, blank=True)
    verdict_type = models.CharField(max_length=3, choices=VerdictType.choices, default=VerdictType.UNTREATED)
    verdict = models.CharField(max_length=500, null=True, blank=True)

    notice_type = models.CharField(max_length=3, choices=NoticeType.choices, default=NoticeType.LOST)
    lost_notice = models.ForeignKey(LostNotice, on_delete=models.DO_NOTHING, related_name='reports',
                                    null=True, blank=True)
    found_notice = models.ForeignKey(FoundNotice, on_delete=models.DO_NOTHING, related_name='reports',
                                     null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    submit_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_reports')

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.notice_type
