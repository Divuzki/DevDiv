from django.core.management.base import BaseCommand
from webpush.models import WebPushNotificationUsers
from django.core.paginator import Paginator
from webpush.views import send_notification
from users.models import Post
from django.conf import settings

DEBUG = settings.DEBUG


class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        # Getting Only Two News And Send It
        paginator = Paginator(Post.objects.all(), 2)
        posts = paginator.page(1)
        if DEBUG == False:
            link = "devdiv.herokuapp.com"
        for post in posts:
            resgistration = []
            qs = WebPushNotificationUsers.objects.all()
            for device in qs:
                resgistration.append(device.registration_id)
            send_notification(resgistration, post.title, post.description,
                              post.image_url, message_link=f"https://{link}/post/{post.id}")
            print(f"sent post: https://{link}/post/{post.id}")
        self.stdout.write('Notification Was Done Sucessfully ✅')
