from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"


class LoginView(TemplateView):
    template_name = "myapp/login.html"

    def get_context_data(self, **kwargs):
        kwargs['clientId'] = "hn9wdfmenh2m4g0d1zwenonvq4yexi"
        kwargs['redirectUrl'] = "http://localhost:8001"
        kwargs['scope'] = "viewing_activity_read+openid"
        return kwargs