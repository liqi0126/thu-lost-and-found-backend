from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import time


class UserStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    INACTIVE = "INA", _('Inactive')
    SUSPENDED = 'SUS', _('Suspended')


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}_{int(time.time())}.{ext}'
    return f'user_avatars/{filename}'


class User(AbstractUser):
    # Inherited fields
    # id, password, username, first_name, last_name, email,
    # is_superuser, is_staff, is_active, last_login,  date_joined
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    student_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    wechat_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=3, choices=UserStatus.choices, default=UserStatus.INACTIVE)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
