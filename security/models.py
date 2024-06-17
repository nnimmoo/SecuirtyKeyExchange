from django.contrib.auth.models import User
from django.db import models

class Channel(models.Model):
    sender_user = models.ForeignKey(User, related_name='sent_channels', on_delete=models.CASCADE)
    recipient_user = models.ForeignKey(User, related_name='received_channels', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    accepted = models.BooleanField(default=False)
    initial_sender_secret = models.BigIntegerField(null=True, blank=True)
    initial_recipient_secret = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
