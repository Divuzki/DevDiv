from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from rest_framework.reverse import reverse as api_reverse
import os
# from PIL import Image

# import required module
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


# CHECKING DB FOR CAT TABLE
category_list = []
# connect to database
con = sqlite3.connect('../divdev.sqlite3')

# create cursor object
cur = con.cursor()

# check if table exists
print('Check if users_category table exists in the database:')
listOfTables = cur.execute(
"""SELECT name FROM sqlite_master WHERE type='table'
AND name='users_category'; """).fetchall()

if listOfTables == []:
	print('Table not found!')
else:
    categories = Category.objects.all().values_list('name', 'name')
    
    for item in categories:
        category_list.append(item)
	# print('Table found!')

# commit changes
con.commit()

# terminate the connection
con.close()


Country = (('Nigeria', 'Nigeria'), ('USA', 'USA'), ('UK', 'UK'),
           ('Ghana', 'Ghana'), ('Canada', 'Canada'))


class HashTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')
    
    def serialize(self):
        return {
            "name": self.name,
        }


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.CharField(
        max_length=3080, default='/static/default_jpg.png')
    status = models.CharField(max_length=50, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(
        choices=Country, max_length=60, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             help_text="Text limit is 250")
    description = models.CharField(max_length=200, null=True, blank=True,
                                   help_text="Text limit is 200, and know that this is the post snippet")
    content = RichTextField()
    # content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255)
    image_url = models.CharField(max_length=3038, null=True, blank=True)
    video_url = models.CharField(max_length=3000, null=True, blank=True)
    category = models.CharField(choices=category_list, max_length=50, default='uncategorized')
    hashtag = models.CharField(max_length=150, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="dislikes",  blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    @property
    def owner(self):
        return self.author

    @property
    def total_likes(self):
        """
        Likes for the post
        :return: Integer: Likes for the post
        """
        return self.likes.count()

    @property
    def total_dislikes(self):
        """
        Dislikes for the post
        :return: Integer: Dislikes for the post
        """
        return self.dislikes.count()

        # For Post Detail

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_api_url(self, request=None):
        api_reverse("post-api:post-api-rud", kwargs={'pk': self.pk}, request=request)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="comments", max_length=255, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(
        User, related_name="comments_likes", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.user)

    def get_post(self):
        return self.post

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "img": self.user.profile.image_url,
            "body": self.body,
            "likes": self.likes.count(),
            "date": self.date_added,
        }


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
