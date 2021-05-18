from django.urls import path

from . import views

urlpatterns = [
    path('', views.DirectView.as_view(), name='base'),
    path('chat/<pk>/', views.ChatView.as_view(), name='chat'),
    path('message/<message_id>/', views.DeleteMessage.as_view(), name='delete')
]
