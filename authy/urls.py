from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='authy/login.html'), name='login'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), {'next_page': 'login'}, name='logout')
]
