from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from rest_framework.reverse import reverse as api_reverse
from django.utils.translation import gettext_lazy as _
from devdiv.utils import image_resize, clean_content


Country = (('Nigeria', 'Nigeria'), ('USA', 'USA'), ('UK', 'UK'),
           ('Ghana', 'Ghana'), ('Canada', 'Canada'))
CategoryList = (('World', 'World'), ('Politics', 'Politics'), ('Technology', 'Technology'), ('Science', 'Science'),
 ('How-To', 'How-To'), ('LifeStyle', 'LifeStyle'), ('Gossip', 'Gossip'))


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
    upload_image = models.ImageField(
        _("Image"), upload_to="profile_images/%Y/%m/", blank=True, null=True)
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
    def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        if self.upload_image:
            image_resize(self.upload_image, 144, 144)


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             help_text="Text limit is 250")
    description = models.CharField(max_length=200,
                                   help_text="Text limit is 200, and know that this is the post snippet")
    content = RichTextField()
    # content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255)
    upload_image = models.ImageField(
        _("Image"), upload_to="post_media/image/%Y/%m/", blank=True, null=True)
    image_url = models.CharField(max_length=3038, null=True, blank=True)
    image_caption = models.CharField(max_length=100, null=True, blank=True,
                                   help_text="Text limit is 100, and know that this is the post image description")
    video_url = models.CharField(max_length=3000, null=True, blank=True)
    category = models.CharField(
        choices=CategoryList, max_length=50, default='uncategorized')
    hashtag = models.CharField(max_length=150, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="dislikes",  blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    @property
    def owner(self):
        return self.author
    
    @property
    def tag(self):
        return self.hashtag

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
        api_reverse("post-api:post-api-rud",
                    kwargs={'pk': self.pk}, request=request)
    
    def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        if self.upload_image:
            image_resize(self.upload_image, 800, 600)
        if self.content:
            self.content = clean_content(self.content, HashTag)



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
