from django_cron import CronJobBase, Schedule
from .models import SocialAuth, EmailNotifications
from social_django.models import UserSocialAuth
import requests
from django.conf import settings
from django.utils import timezone
import json
from myapp.email import SendEmail

class StreamCronJob(CronJobBase):
    """
    We Will Send Stream Online Email only if user has not received same channel stream email within his current session.
    """

    RUN_EVERY_MINS = 1 # every 2 mins
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.stream'

    def do(self):
        """
        Sends Email Notification on Channel Upstream
        """
        url = 'https://api.twitch.tv/kraken/streams/followed'
        all_users = UserSocialAuth.objects.all()
        headers = {
            'Client-ID': settings.SOCIAL_AUTH_TWITCH_KEY,
            "Accept": "application/vnd.twitchtv.v5+json"
        }
        allSubsIds = []
        # Checking All Users
        for userObj in all_users:

            if userObj.extra_data['access_token']:
                # Getting User Settings
                social_auth_instance = SocialAuth.objects.get(user_id=userObj.user.id)


                # Getting Online Streams
                accessToken = userObj.extra_data['access_token']
                headers['Authorization'] = "OAuth {0}".format(accessToken)
                request = requests.get(url, headers=headers)

                if request.status_code == 200:
                    allSubscribedChannels = request.json()['streams']

                    # Checking All Online Channels
                    for channel in allSubscribedChannels:

                        channelDetail = self.getChannelData(channel)
                        allSubsIds = list(map(lambda x: x['_id'], allSubscribedChannels))

                        channelData = social_auth_instance.social_auth.filter(
                            last_sent_channel_id = channel['_id'],
                            is_online=True,
                            notification_about = 1
                        )

                        if not channelData.exists():
                            # If This Channel has no last instance in EmailNotifications table and is Currently Offline, then create Instance
                            en = EmailNotifications.objects.create(
                                social_auth = social_auth_instance,
                                last_sent_channel_id = channelDetail['id'],
                                subject = channelDetail["content"],
                                is_online = True,
                                notification_about = 1
                            )
                            en.save()
                            SendEmail.send(channelDetail)


                    # Reset is_online for All Related Non Live Channels
                    relatedEmailObjNotInList = social_auth_instance.social_auth.\
                        filter(notification_about=1).\
                        exclude(last_sent_channel_id__in = allSubsIds).all()

                    relatedEmailObjNotInList.update(is_online = False)



    def getChannelData(self, channel):

        channelDetail = {
            "display_name": channel['channel']['display_name'],
            "id": channel['_id'],
            "notification_about": 1, #Stream
            "content": "Channel {0} just started Streaming".format(channel['channel']['display_name']),
            "subject": "Channel Started Streaming"
        }
        return channelDetail



class FollowerCronJob(CronJobBase):
    """
    Sends Email Notification on New Follower
    """
    RUN_EVERY_MINS = 1 # every 2 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.follower'

    def do(self):
        url = 'https://api.twitch.tv/helix/users/follows'
        all_users = UserSocialAuth.objects.all()
        headers = {
            'Client-ID': settings.SOCIAL_AUTH_TWITCH_KEY
        }

        # Checking All Users
        for userObj in all_users:
            user_uid = userObj.uid

            if userObj.extra_data['access_token']:
                # Getting User Settings
                social_auth_instance = SocialAuth.objects.get(user_id=userObj.user.id)
                #Getting Followers list from DB
                myFollowers = ([], json.loads(social_auth_instance.followers))[bool(social_auth_instance.followers)]

                payload = {'to_id' : user_uid}

                allFollowedUsers = requests.get(url, headers=headers, params=payload).json()['data']


                for follower in allFollowedUsers:

                    if follower['from_id'] not in myFollowers:
                        myFollowers.append(follower['from_id'])
                        social_auth_instance.followers = json.dumps(myFollowers)
                        social_auth_instance.save()
                        userData = self.getUserData(follower['from_id'], headers)

                        en = EmailNotifications.objects.create(
                            social_auth=social_auth_instance,
                            subject=userData["content"],
                            notification_about=userData["notification_about"]
                        )
                        en.save()
                        SendEmail.send(userData)

    def getUserData(self,userId, headers):
        userData = {}
        url = "https://api.twitch.tv/helix/users"
        payload = {"id": userId}

        userData["id"] = userId
        userData["display_name"] = requests.get(url, headers = headers, params=payload).json()['data'][0]['display_name']
        userData["content"] = "User {0} has just started following you".format(userData["display_name"])
        userData["notification_about"] = 2
        userData["subject"] = "You have a new Follower"

        return userData