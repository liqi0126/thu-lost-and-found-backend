from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    create_at = models.DateTimeField(default=timezone.now)

