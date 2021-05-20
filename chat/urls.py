from django.urls import path

from . import views

urlpatterns = [
    path('', views.DirectView.as_view(), name='base'),
    path('chat/<pk>/', views.ChatView.as_view(), name='chat'),
    path('message/<message_id>/', views.ChangeMessage.as_view(), name='change'),
    path('message-delete/<message_id>/<option>/', views.DeleteMessage.as_view(), name='delete'),
    path('new-chat/<user_id>/', views.StartChat.as_view(), name='start_chat')
]
