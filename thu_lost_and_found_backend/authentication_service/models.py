import time

from django.db import models

from thu_lost_and_found_backend.user_service.models import User


def supporting_document_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'user_{instance.user}_supporting_document_{int(time.time())}.{ext}'
    return f'user_verification_application/{filename}'


class UserVerificationApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_application')
    description = models.CharField(max_length=300, default=None)
    supporting_document = models.ImageField(upload_to=supporting_document_upload_path, null=True, blank=True)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
