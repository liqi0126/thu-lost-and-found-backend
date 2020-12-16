from django.db import models
from thu_lost_and_found_backend.user_service.models import User


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='received_messages')
    message = models.TextField()
    sent = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.message
