from django.db import models
from django.utils import timezone
from django.core import validators


class Notice(models.Model):
    create_at = models.DateTimeField(default=timezone.now)
    edit_at = models.DateTimeField()
    photo = models.ImageField()
    descriptions = models.TextField()
    phone = models.CharField(validators=[validators.RegexValidator("1[345678]\d{9}",message='Please Enter the right phone number!')],
                             max_length=20)
    wechat = models.CharField(max_length=30)

    # TODO: form of verification question?
    # TODO: time: a period of time?
    # TODO: place: a list of places?

    # TODO: use a boolean value to indicate status ?
    padding = models.BooleanField(default=False)

    class Meta:
        app_label = 'notice'
