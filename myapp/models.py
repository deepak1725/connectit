from django.db import models
from django.contrib.auth.models import User


# Settings Table
class SocialAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(null=True, blank=True)
    email_notifications = models.BooleanField()
    text_notifications = models.BooleanField(default=False)
    followers = models.TextField(default=[])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



# Data Table
class EmailNotifications(models.Model):
    social_auth = models.ForeignKey(SocialAuth, on_delete=models.CASCADE, related_name='social_auth')
    # 1 => Stream Online Notification, 2 => User Follow Notifications
    notification_about = models.IntegerField(default=1)
    is_online = models.NullBooleanField(default=False, null=True)
    last_sent_channel_id = models.TextField(null=True)
    subject = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


