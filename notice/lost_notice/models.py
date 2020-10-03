from django.db import models
from notice.model import Notice

from django.conf import settings
from property.models import Property


class LostNotice(Notice):
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_notices')
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='lost_notice')
