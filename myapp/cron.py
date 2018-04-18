from django_cron import CronJobBase, Schedule
from .models import SocialAuth, EmailNotifications
from social_django.models import UserSocialAuth
import requests
from django.conf import settings
from django.utils import timezone


class StreamCronJob(CronJobBase):
    """
    We Will Send Stream Online Email only if user has not received same channel stream email with in last 30 Mins.
    """

    RUN_EVERY_MINS = 1 # every 2 mins
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.stream'

    def do(self):
        url = 'https://api.twitch.tv/kraken/streams/followed'
        all_users = UserSocialAuth.objects.all()
        print("Ran")
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
                    print(allSubscribedChannels)

                    # Checking All Online Channels
                    for channel in allSubscribedChannels:
                        channelDetail = {
                            "display_name" : channel['channel']['display_name'],
                            "id" : channel['_id']
                        }
                        allSubsIds = list(map(lambda x: x['_id'], allSubscribedChannels))
                        print(allSubsIds)

                        emailData = social_auth_instance.social_auth\
                            .filter(last_sent_channel_id = channel['_id'])

                        if emailData.exists():
                            sendToData = emailData.filter(updated__minute__gte = 30)

                            if sendToData.exists():
                                self.sendEmail()

                            sendToData = sendToData.first()
                            sendToData['last_sent_channel_id'] = channel['_id']
                            sendToData.is_online = True
                            sendToData.updated = timezone.now()
                            sendToData.created = timezone.now()
                            sendToData.save()

                            print("Data Updated")

                        else:
                            # If This Channel has no instance in EmailNotifications table, create Instance
                            print("Creating Instance")
                            en = EmailNotifications.objects.create(
                                social_auth = social_auth_instance,
                                last_sent_channel_id = channel['_id'],
                                subject = "Hey Baby",
                                is_online = True
                            )
                            en.save()

                            self.sendEmail()


                    # Reset is_online for All Related Non Live Channels
                    relatedEmailObjNotInList = social_auth_instance.social_auth.\
                        exclude(last_sent_channel_id__in = allSubsIds).all()

                    relatedEmailObjNotInList.update(is_online = False)

                    print("Saved")

                else:
                    print("Token Expired")


        print("Execution Complete")

    def sendEmail(self):
        print("Email Send")


class NewFollowerCheckCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.follower'

    def do(self):
        pass