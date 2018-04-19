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


class FollowerCallbackView(View):

    def get(self, request):
        challenge = request.GET.get("hub.challenge", None)
        return HttpResponse(challenge, status=200)


    def post(self, request, *args, **kwargs):
        print("in Follower post")

        data = request.GET.get("data", None)
        data = data[0]
        twitchUserId = data['to_id']
        followerId = data['from_id']
        userEmail, social_auth_instance = GetUserEmail.fetchEmail(twitchUserId)
        emailData = {}
        emailData['userEmail'] = userEmail
        emailData['subject'] = "You have a new Follower"
        emailData['content'] = "{0} started following you.".format("User")
        en = EmailNotifications.objects.create(
            social_auth = social_auth_instance,
            subject = emailData['subject'],
            notification_about = 2
        )
        en.save()
        email = SendEmail.send(emailData)
        print("FollowerReturned")
        return HttpResponse("Success",status=200)


class GetUserEmail():
    def fetchEmail(twitchUserId):
        social_auth_instance = UserSocialAuth.objects.get(uid=twitchUserId)
        userId = social_auth_instance.user_id
        user = User.objects.get(id=userId)
        return (user.email, social_auth_instance)


class StreamCallbackView(View):

    def get(self, request):
        challenge = request.GET.get("hub.challenge", None)
        return HttpResponse(challenge, status=200)


    def post(self, request, *args, **kwargs):
        print("in Webhook Strean post")
        data = request.GET.get("data", None)
        data = data[0]
        twitchUserId = data.user_id
        channelTitle = data.title
        userEmail, social_auth_instance = GetUserEmail.fetchEmail(twitchUserId)

        emailData = {}

        emailData['subject'] = "A Subscribed stream went Online"
        emailData['content'] = "{0} has just started streaming".format(channelTitle)
        emailData['userEmail'] = userEmail

        en = EmailNotifications.objects.create(
            social_auth = social_auth_instance,
            subject = emailData['subject'],
            notification_about = 1
        )
        en.save()

        email = SendEmail.send(emailData)

        print("StreamReturned")
        return HttpResponse("Success",status=200)




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

        if not socialAuth.exists():
            form.save()


        if form.instance.email_notifications:
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
                "hub.callback" : "http://f21c5cae.ngrok.io/callback/follower/?notification_about={0}&sa={1}&userEmail={2}".format(
                    2, socialAuth.id, self.request.user.email),
                "hub.mode" : "subscribe",
                "hub.topic" : "https://api.twitch.tv/helix/users/follows?first=1&to_id={0}".format(authUser.uid)
            }
            response = requests.post(url, data=followerPayload, headers=headers)


            # Stream Payload
            streamPayload = {
                "hub.callback": "http://f21c5cae.ngrok.io/callback/stream/?notification_about={0}&sa={1}".format(1, socialAuth.id),
                "hub.mode": "subscribe",
                "hub.topic": "https://api.twitch.tv/helix/streams?user_id={0}".format(authUser.uid)
            }
            response = requests.post(url, data=streamPayload, headers=headers)


        return super().form_valid(form)