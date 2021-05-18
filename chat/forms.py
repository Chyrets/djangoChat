from django import forms

from chat.models import Message


class MessageForm(forms.ModelForm):
    """
    Send message form
    """

    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
