from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView,View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import requests


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"


class LoginView(TemplateView):
    template_name = "myapp/login.html"

    def get_context_data(self, **kwargs):
        kwargs['clientId'] = "hn9wdfmenh2m4g0d1zwenonvq4yexi"
        kwargs['redirectUrl'] = "http://localhost:8001/auth"
        kwargs['scope'] = "channel_read%20channel_stream%20openid%20user_read"
        kwargs['responseType'] = "code"
        return kwargs

class AuthView(View):
    def get(self, request):
        code = request.GET.get('code', None)
        scope = request.GET.get('scope', None)
        state = request.GET.get('state', None)
        if code:
            # Getting Assess Token
            payload = {
                'client_id': 'hn9wdfmenh2m4g0d1zwenonvq4yexi',
                'client_secret': 'iiomcyjvzexattlpyrj6vx0h9xthvr',
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:8001/auth',
            }
            r = requests.post('https://id.twitch.tv/oauth2/token', data=payload)
            # print("Json")
            print(r.json())

            if r.status_code == 200:
                #Getting status of Token and UserId
                r = r.json()
                url = 'https://api.twitch.tv/kraken/user'
                headers = {
                    'Accept': 'application/vnd.twitchtv.v5+json',
                    'Authorization': "OAuth {}".format(r['access_token']),
                    'Client-ID': "hn9wdfmenh2m4g0d1zwenonvq4yexi",
                }
                userObj = requests.get(url, headers=headers)

                if userObj.status_code == 200:
                    userObj = userObj.json()
                    # userUrl = userObj['user_id']

                    # user = requests.get(url, headers=headers)
                    print(userObj)

        return HttpResponse("GET")

    def post(self, request):
        print("In Post")
        return HttpResponse("Post")