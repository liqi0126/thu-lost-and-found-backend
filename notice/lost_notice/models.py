from django.db import models
from notice.model import Notice

from django.conf import settings


class LostNotice(Notice):
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_notices')
    properties