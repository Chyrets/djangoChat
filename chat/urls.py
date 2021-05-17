from django.urls import path

from . import views

urlpatterns = [
    path('', views.DirectView.as_view(), name='base'),
    path('chat/<username>/', views.GetMessageView.as_view(), name='direct'),
    path('chat/<username>/send/', views.SendMessageView.as_view(), name='send')
]
