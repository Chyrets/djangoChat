from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
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
                messages.append({
                    'last_message': chat.message_set.filter(deleted=False).exclude(
                        deleted_for_user=request.user).latest('date'),
                    'unread': chat.message_set.filter(unread=True).count(),
                    'chat': chat.pk
                })
            except Message.DoesNotExist:
                continue

        messages = sorted(messages, key=lambda message: message['last_message'].date, reverse=True)

        context = {
            'chats': chats,
            'messages': messages
        }

        return render(request, self.template_name, context)


class DialogView(LoginRequiredMixin, View):
    """
    Display dialog with some user
    """
    form_class = MessageForm
    template_name = 'chat/direct.html'

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        messages = Message.objects.filter(chat_id=pk, chat__members=user, deleted=False).exclude(deleted_for_user=user)
        chat = Chat.objects.get(id=pk)

        for message in messages:
            if message.author != user:
                message.unread = False
                message.save()

        form = self.form_class()
        users = User.objects.exclude(username=user)

        context = {
            'messages': messages,
            'form': form,
            'users': users,
            'chat': chat
        }

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        chat = Chat.objects.get(id=pk)
        user = request.user

        if 'send' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.chat_id = pk
                message.author = user
                if request.POST.get('parent', None):
                    message.parent_id = int(request.POST.get('parent'))
                message.save()

        if chat.type == chat.CHAT and chat.admin == user:
            if 'add' in request.POST:
                chat.members.add(*request.POST.getlist('members'))
            elif 'delete' in request.POST:
                chat.members.remove(*request.POST.getlist('members'))

        return redirect(reverse('chat', args=pk))


class DeleteMessage(LoginRequiredMixin, View):
    """
    Display buttons for deleting message
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request, option, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)

        if int(option) == 0:
            message.deleted_for_user = request.user
            message.save()
        else:
            message.deleted = True
            message.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeMessage(LoginRequiredMixin, View):
    """
    Display page for change message
    """

    def get(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id, author=request.user)
        return render(request, 'chat/change_message.html', {'message': message})

    def post(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id, author=request.user)
        form = MessageForm(request.POST)

        if form.is_valid():
            message.message = form.cleaned_data.get('message')
            message.changed = True
            message.save()

        return redirect('chat', pk=message.chat_id)


class StartDialog(LoginRequiredMixin, View):
    """
    Start dialog with some user
    """

    def get(self, request, user_id):
        chat = Chat.objects.filter(members__in=[request.user.pk, int(user_id)], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chat.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chat.first()
        return redirect('chat', chat.pk)


class StartChat(LoginRequiredMixin, View):
    """
    Start chat with several user
    """

    def get(self, request):
        chat = Chat.objects.create(admin=request.user, type=Chat.CHAT)
        chat.members.add(request.user)
        return redirect('chat', chat.pk)
