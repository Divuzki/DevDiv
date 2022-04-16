from django.core.management.base import BaseCommand
from webpush.models import WebPushNotificationUsers
from django.core.paginator import Paginator
from webpush.views import send_notification
from users.models import Post
from django.conf import settings
ALLOWED_HOSTS = settings.ALLOWED_HOSTS[0]
DEBUG = settings.DEBUG
if DEBUG == True:
    ALLOWED_HOSTS = 'localhost:8000'


class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        # Getting Only Two News And Send It
        paginator = Paginator(Post.objects.all(), 2)
        posts = paginator.page(1)
        for post in posts:
            resgistration = []
            qs = WebPushNotificationUsers.objects.all()
            for device in qs:
                resgistration.append(device.registration_id)
            send_notification(resgistration, post.title, post.description,
                              post.image_url, message_link=f"//{ALLOWED_HOSTS}/post/{post.id}")
        self.stdout.write('Notification Was Done Sucessfully ✅')
