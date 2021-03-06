from django.shortcuts import render
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
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
import os



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"




class LoginView(TemplateView):
    template_name = "myapp/login.html"

class FollowerCallbackView(View):

    def get(self, request):
        challenge = request.GET.get("hub.challenge", None)
        emailData = {}
        emailData['subject'] = "Welcome to Connectit | Successfully Subscribed"
        emailData['content'] = "Somebody on roll"
        emailData['userEmail'] = "sharma1725@gmail.com"
        email = SendEmail.send(emailData)

        return HttpResponse(challenge, status=200)


    def post(self, request, *args, **kwargs):
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
        return HttpResponse("Success",status=200)



class UserDetailsView(LoginRequiredMixin, FormView):
    template_name = "myapp/user_details.html"
    form_class = SocialAuthForm

    def get_success_url(self, **kwargs):
        if self.request.session.get('from_social_auth', None):
            return reverse('social:complete', args = ("twitch", ))
        return reverse('myapp:index')

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
            authUser = UserSocialAuth.objects.get(user_id=self.request.user.id)

            headers = {
                'Client-ID': settings.SOCIAL_AUTH_TWITCH_KEY,
                "Accept": "application/vnd.twitchtv.v5+json"
            }

            # Follower Payload
            followerPayload = {
                "hub.callback" : self.request.build_absolute_uri(reverse('myapp:follower')),
                "hub.mode" : "subscribe",
                "hub.topic" : "https://api.twitch.tv/helix/users/follows?first=1&to_id={0}".format(authUser.uid),
                "hub.lease_seconds": 864000, #10 Days,
            }
            
            url = "https://api.twitch.tv/helix/webhooks/hub"
            response = requests.post(url, data=followerPayload, headers=headers)

            # Stream Payload
            streamPayload = {
                "hub.callback": self.request.build_absolute_uri(reverse('myapp:stream')),
                "hub.mode": "subscribe",
                "hub.topic": "https://api.twitch.tv/helix/streams?user_id={0}".format(authUser.uid),
                "hub.lease_seconds": 864000, #10 Days
            }
            response = requests.post(url, data=streamPayload, headers=headers)
            self.confirmUser(self.request.user.email)

        return super().form_valid(form)


    def confirmUser(self, email):
        emailData = {}
        emailData['subject'] = "Welcome to Connectit | Successfully Subscribed"
        emailData['content'] = "We are glad that you came. Your subscription is successfully activated."
        emailData['userEmail'] = email
        emailIt = SendEmail.send(emailData)
        return

"""

    ------------------------------  API  -----------------------

"""

class GetUserDetailsApi(APIView):
    permission_classes = ''

    def get(self, request, format=None):

        userSocial = UserSocialAuth.objects.filter(user_id = request.user.id).first()
        mySocialAuth = SocialAuth.objects.filter( user_id = request.user.id).first()

        notifications = mySocialAuth.social_auth.select_related().order_by('-created')
        totalStreamEmails = notifications.filter(notification_about = 1).count()
        totalUserFollowEmails = notifications.filter(notification_about = 2).count()

        notificationsData = []
        for notification in notifications.all():
            data = {
                'id' : notification.id,
                'subject' : notification.subject,
                'notification_about' : notification.notification_about,
                'sent_on' : notification.created
            }
            notificationsData.append(data)

        payload = {
            'username' : request.user.username,
            'connectedThrough' : userSocial.provider.title(),
            'membersince': mySocialAuth.created,
            'totalStreamEmails': totalStreamEmails,
            'totalUserFollowEmails': totalUserFollowEmails,
            'notificationsData': notificationsData
        }

        responseData = {
            'message': 'Details Successfuly fetched',
            'data': payload,
            'error': None
        }
        return Response(responseData, status=status.HTTP_200_OK)