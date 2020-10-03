from django.db import models
from django.utils import timezone
from django.core import validators
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    create_at = models.DateTimeField(default=timezone.now)

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(validators=[validators.RegexValidator("1[345678]\d{9}",message='Please Enter the right phone number!')],
                             max_length=20)
    school_id = models.CharField(validators=[validators.RegexValidator("[12]\d{9}",message='Please Enter the right school id!')],
                             max_length=10, unique=True)
    avatar = models.ImageField()

    # foreign key
    # found_notices
    # lost_notices
