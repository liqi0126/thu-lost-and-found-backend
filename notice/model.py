from django.db import models
from django.utils import timezone

class Notice(models.Model):
    create_at = models.DateTimeField(default=timezone.now)
