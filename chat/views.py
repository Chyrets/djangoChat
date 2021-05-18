from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from chat.forms import MessageForm
from chat.models import Message, Chat


class DirectView(LoginRequiredMixin, View):
    """
    Main page with all directs
    """
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(members=request.user)

        messages = []
        for chat in chats:
            try:
                messages.append(Message.objects.filter(chat=chat).latest('date'))
            except Message.DoesNotExist:
                continue

        messages = sorted(messages, key=lambda message: message.date, reverse=True)

        context = {
            'chats': chats,
            'messages': messages
        }

        return render(request, self.template_name, context)


class ChatView(LoginRequiredMixin, View):
    """
    Display chat with some user
    """
    form_class = MessageForm
    template_name = 'chat/direct.html'

    def get(self, request, pk, *args, **kwargs):
        messages = Message.objects.filter(chat_id=pk, chat__members=request.user, deleted=False)

        form = self.form_class()

        context = {
            'messages': messages,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = pk
            message.author = request.user
            message.save()

        return redirect(reverse('chat', args=pk))


class DeleteMessage(LoginRequiredMixin, View):
    """
    Display page with choices how to delete message
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)
        if request.method == 'POST':
            message.deleted = True
            message.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
