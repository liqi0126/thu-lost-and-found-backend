from django.db import models
from django.utils.translation import gettext_lazy as _

from thu_lost_and_found_backend.user_service.models import User


class ContactMethod(models.TextChoices):
    PHONE = 'PHN', _('Phone')
    WECHAT = "WCT", _('Wechat')
    EMAIL = 'EML', _('Email')


class Contact(models.Model):
    name = models.CharField(max_length=30, default='Anonymous')
    method = models.CharField(max_length=3, choices=ContactMethod.choices, default=ContactMethod.WECHAT)
    details = models.CharField(max_length=50, default=None)

    # TODO: enable auth
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'contact'
