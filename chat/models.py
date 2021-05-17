from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """
    Message from one user to another
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=420)
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        return f"from {self.sender} to {self.recipient}"
