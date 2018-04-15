from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView,View, FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SocialAuthForm

class IndexView(TemplateView):
    template_name = "myapp/index.html"


class LoginView(TemplateView):
    template_name = "myapp/login.html"


class UserDetailsView(FormView):
    template_name = "myapp/user_details.html"
    form_class = SocialAuthForm
    success_url = '/thanks/'

    def form_valid(self, form):
        thought = form.save(commit=False)
        thought.user = self.request.user
        thought.save()
