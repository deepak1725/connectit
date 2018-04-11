from django.db import models
from django.contrib.auth.models import User



class SocialAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    access_token = models.CharField(max_length=50, null=False)
    expires_in = models.CharField(max_length=50, null=False)
    refresh_token = models.CharField(max_length=50, null=False)
    scope = models.CharField(max_length=50, null=False)

    auth_id = models.CharField(max_length=50, null=False)
    email_notifications = models.BooleanField()
    created_at = models.DateTimeField(null=False)
    updated_at = models.DateTimeField(null=False)

