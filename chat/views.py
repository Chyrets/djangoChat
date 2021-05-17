from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from chat.models import Message


class DirectView(LoginRequiredMixin, View):
    """
    Main page with all directs
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'chat/base.html', {})


class GetMessageView(LoginRequiredMixin, View):
    """
    Display message from some user
    """

    def get(self, request, username, *args, **kwargs):
        messages_from = Message.objects.filter(recipient=request.user, sender__username=username)
        message_to = Message.objects.filter(recipient__username=username, sender=request.user)
        messages = message_to.union(messages_from, all=True).order_by('date')

        context = {
            'messages': messages,
            'username': username,
        }

        return render(request, 'chat/direct.html', context)


class SendMessageView(LoginRequiredMixin, View):
    """
    Display form for sending message
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def post(self, request, username, *args, **kwargs):
        from_user = request.user
        to_user = User.objects.get(username=username)
        body = request.POST.get('body')

        send_message = Message(sender=from_user, recipient=to_user, body=body)
        send_message.save()

        return redirect('direct', username)
