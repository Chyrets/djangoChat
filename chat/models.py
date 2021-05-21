from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    """
    Chat rom for user
    """
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'DIALOG'),
        (CHAT, 'CHAT')
    )
    type = models.CharField(max_length=1, choices=CHAT_TYPE_CHOICES)
    members = models.ManyToManyField(User)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialog_admin', null=True, blank=True)


class Message(models.Model):
    """
    Message from one user to another
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    message = models.TextField(max_length=420, null=True)
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_for_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    changed = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='message_parent', null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.message
