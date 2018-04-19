from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView,View, FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import SocialAuthForm
from django.urls import reverse_lazy, reverse
from .models import SocialAuth, EmailNotifications
import requests
from django.conf import settings
from social_django.models import UserSocialAuth
from django.http import HttpResponse
from myapp.email import SendEmail
import os

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"


class LoginView(TemplateView):
    template_name = "myapp/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('index')

        return render(request, self.template_name,{})




class WebhookDataReturnView(View):

    def get(self, request, *args, **kwargs):
        print("in Webhook get")
        response = {}
        response['challenge'] = request.GET.get("hub.challenge", None)
        response['lease_seconds'] = request.GET.get("hub.lease_seconds", None)
        response['mode'] = request.GET.get("hub.mode", None)
        response['topic'] = request.GET.get("hub.topic", None)
        response['saId'] = request.GET.get("sa", None)
        response['userEmail'] = request.GET.get("userEmail", None)
        response['notification_about'] = request.GET.get("notification_about", None)

        social_auth_instance = SocialAuth.objects.get(id=response['saId'])

        emailData = {}

        emailData['subject'] = "Channel went Online"
        emailData['content'] = "Channel you followed has just started streaming"
        emailData['userEmail'] = response['userEmail']

        if int(response['notification_about']) == 1:
            print("In if")
            emailData['subject'] = "You have a new Follower"
            emailData['content'] = "User started following you."

        en = EmailNotifications.objects.create(
            social_auth = social_auth_instance,
            subject = emailData['subject'],
            notification_about = response['notification_about']
        )
        en.save()

        email = SendEmail.send(emailData)

        print(response)
        print("Returned")
        return HttpResponse(status=200)




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
        socialAuth = SocialAuth.objects.filter(user_id = self.request.user.id)
        # print(os.environ["SENDGRID_KEY"])
        if not socialAuth.exists():
            print("Savinf")
            form.save()

        # Subscribe to webhooks
        url = "https://api.twitch.tv/helix/webhooks/hub"
        authUser = UserSocialAuth.objects.get(user_id=self.request.user.id)

        socialAuth = socialAuth.first()
        headers = {
            'Client-ID': settings.SOCIAL_AUTH_TWITCH_KEY,
            "Accept": "application/vnd.twitchtv.v5+json"
        }

        # Follower Payload
        followerPayload = {
            "hub.callback" : "http://d9d755a9.ngrok.io/webhook/?notification_about={0}&sa={1}&userEmail={2}".format(
                2, socialAuth.id, self.request.user.email),
            "hub.mode" : "subscribe",
            "hub.topic" : "https://api.twitch.tv/helix/users/follows?first=1&to_id={0}".format(authUser.uid)
        }
        response = requests.post(url, data=followerPayload, headers=headers)


        # Stream Payload
        streamPayload = {
            "hub.callback": "http://d9d755a9.ngrok.io/webhook/?notification_about={0}&sa={1}".format(1, socialAuth.id),
            "hub.mode": "subscribe",
            "hub.topic": "https://api.twitch.tv/helix/streams?user_id={0}".format(authUser.uid)
        }
        response = requests.post(url, data=streamPayload, headers=headers)


        return super().form_valid(form)