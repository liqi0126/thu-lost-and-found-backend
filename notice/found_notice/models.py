from django.db import models
from notice.model import Notice
from user.models import User


class FoundNotice(Notice):
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='found_notices')
