from django.shortcuts import redirect
from social_core.pipeline.partial import partial
from .models import SocialAuth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@partial
def show_user_details(strategy, backend, request, details, *args, **kwargs):
    request.session["details"] = details

    if not request.user.is_authenticated:
        user = User.objects.get(email__exact=details['email'])
        login(request,user,'django.contrib.auth.backends.ModelBackend')
    exists_in_auth = SocialAuth.objects.filter(user_id=request.user.id).exists()
    if not exists_in_auth:
        return redirect("details")
