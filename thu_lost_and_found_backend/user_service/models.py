from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from thu_lost_and_found_backend.helpers.toolkits import timestamp_filename


class UserStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    INACTIVE = "INA", _('Inactive')
    SUSPENDED = 'SUS', _('Suspended')


def image_upload_path(instance, filename):
    model_name = instance.__class__.__name__
    folder_name = ''
    ext = filename.split('.')[-1]

    if model_name == User.__name__:
        folder_name = 'user_avatars'
        filename = timestamp_filename(instance.username, ext)
    elif model_name == UserVerificationApplication.__name__:
        folder_name = 'user_verification_application'
        filename = timestamp_filename(f'user_{instance.user.username}_supporting_document', ext)

    return f'{folder_name}/{filename}'


class User(AbstractUser):
    # Inherited fields
    # id, password, username, first_name, last_name, email,
    # is_superuser, is_staff, is_active, last_login, date_joined
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    username = models.CharField(max_length=125)
    email = models.EmailField(unique=True, max_length=125, null=True, blank=True)
    avatar = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    wechat_avatar = models.CharField(max_length=225, null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    student_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    department = models.CharField(max_length=20, null=True, blank=True)
    wechat_openid = models.CharField(max_length=50, null=True, blank=True, unique=True)
    wechat_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    channel_name = models.CharField(max_length=150, null=True, blank=True, unique=True)

    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=3, choices=UserStatus.choices, default=UserStatus.INACTIVE)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
            return self.username

class UserRole(models.TextChoices):
    # Super admin
    ADMIN = 'ADM', _('Admin')
    STAFF = 'STF', _('Staff')
    USER = 'USR', _('User')


class UserInvitation(models.Model):
    role = models.CharField(max_length=3, choices=UserRole.choices, default=UserRole.USER)
    email = models.EmailField(unique=True, max_length=125, null=False, blank=False)
    token = models.CharField(max_length=64, null=False, blank=False, unique=True)
    expiration_date = models.DateTimeField(null=False, blank=False)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class UserEmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification')
    email = models.EmailField(unique=True, max_length=125, null=False, blank=False)
    token = models.CharField(max_length=64, null=False, blank=False, unique=True)
    expiration_date = models.DateTimeField(null=False, blank=False)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class UserVerificationApplicationStatus(models.TextChoices):
    # Super admin
    ACCEPT = 'ACC', _('Accept')
    REJECT = 'REJ', _('Reject')
    TBD = 'TBD', _('ToBeDetermined')


class UserVerificationApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_application')
    description = models.CharField(max_length=300, default=None)
    supporting_document = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    status = models.CharField(max_length=3, choices=UserVerificationApplicationStatus.choices,
                              default=UserVerificationApplicationStatus.TBD, blank=True)

    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
