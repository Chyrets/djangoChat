from django.contrib import admin

from chat.models import Message, Chat

admin.site.register(Chat)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'deleted')
