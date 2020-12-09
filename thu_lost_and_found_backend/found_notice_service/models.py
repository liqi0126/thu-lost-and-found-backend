from django.db import models
from django.utils.translation import gettext_lazy as _
from thu_lost_and_found_backend.contact_service.models import Contact
from thu_lost_and_found_backend.property_service.models import Property
from thu_lost_and_found_backend.user_service.models import User


class FoundNoticeStatus(models.TextChoices):
    RETURN = 'RET', _('Return')
    PUBLIC = 'PUB', _('Public')
    CLOSE = 'CLS', _('Close')
    DRAFT = 'DFT', _('Draft')


class FoundNotice(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='found_notice')
    images = models.JSONField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    found_datetime = models.DateTimeField()
    found_location = models.JSONField(null=False, blank=False)

    quizzes = models.JSONField(null=True, blank=True)
    contacts = models.ManyToManyField(Contact, related_name='found_notices', default=None)

    status = models.CharField(max_length=3, choices=FoundNoticeStatus.choices, default=FoundNoticeStatus.PUBLIC)

    return_user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True,
                                    related_name='returned_lost_property_notices')
    return_datetime = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='found_notices')

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
