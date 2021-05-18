from django.contrib.auth.mixins import LoginRequiredMixin
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

        context = {
            'chats': chats,
        }

        return render(request, self.template_name, context)


class ChatView(LoginRequiredMixin, View):
    """
    Display chat with some user
    """
    form_class = MessageForm
    template_name = 'chat/direct.html'

    def get(self, request, pk, *args, **kwargs):
        messages = Message.objects.filter(chat_id=pk, chat__members=request.user)

        form = self.form_class()

        context = {
            'messages': messages,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = pk
            message.author = request.user
            message.save()

        return redirect(reverse('chat', args=pk))
