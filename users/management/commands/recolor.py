from django.core.management.base import BaseCommand
from users.models import Post
from devdiv.utils import get_image_color



class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        # Getting Only Two News And Send It
        
        posts = Post.objects.all()
        for post in posts:
            post.image_color = get_image_color(post.image_url)
            post.save()
            print(f"{post.image_url} has been colored 😁")
        self.stdout.write('Added Colors Sucessfully ✅')
