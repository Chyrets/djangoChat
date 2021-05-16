from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from authy.forms import UserSignupForm


class UserSignupView(CreateView):
    """
    User signup view
    """
    model = User
    form_class = UserSignupForm
    success_url = '/'
    template_name = 'authy/signup.html'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid
