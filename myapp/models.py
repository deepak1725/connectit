from django.db import models
from django.contrib.auth.models import User



class SocialAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    mobile = models.IntegerField(null=True, blank=True)
    email_notifications = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

