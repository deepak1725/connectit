from django.core.mail import send_mail

class SendEmail():

    def send(data):
        send_mail(
            subject=data['subject'],
            message=data['content'],
            from_email='admin@connectit.com',
            recipient_list=["sharma1725@gmail.com", data["userEmail"]],
            fail_silently=False
        )
        return