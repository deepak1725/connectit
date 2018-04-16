from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView,View, FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import SocialAuthForm
from django.urls import reverse_lazy, reverse
from .models import SocialAuth


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"


class LoginView(TemplateView):
    template_name = "myapp/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('index')

        return render(request, self.template_name,{})


class UserDetailsView(LoginRequiredMixin, FormView):
    template_name = "myapp/user_details.html"
    form_class = SocialAuthForm

    def get_success_url(self, **kwargs):
        if self.request.session.get('from_social_auth', None):
            return reverse('social:complete', args = ("twitch", ))
        return reverse('index')

    def get_initial(self):
        context = super(UserDetailsView, self).get_initial()
        details = self.request.session['details']
        context['name'] = details['username']
        context['email'] = details['email']
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        exists = SocialAuth.objects.filter(user_id=self.request.user.id).exists()

        if not exists:
            form.save()

        return super().form_valid(form)