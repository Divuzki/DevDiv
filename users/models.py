import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from rest_framework.reverse import reverse as api_reverse
from django.utils.translation import gettext_lazy as _
from devdiv.utils import image_resize, check_for_tag, get_image_color
from taggit.managers import TaggableManager
from taggit.models import Tag

STATIC_URL = settings.STATIC_URL
MEDIA_URL = settings.MEDIA_URL

Country = (('Nigeria', 'Nigeria'), ('USA', 'USA'), ('UK', 'UK'),
           ('Ghana', 'Ghana'), ('Canada', 'Canada'))
CategoryList = (('uncategorized', 'uncategorized'), ('foreign', 'foreign'), ('local', 'local'),
                ('sports', 'sports'), ('politics',
                                       'politics'), ('technology', 'technology'),
                ('science', 'science'), ('finace',
                                         'finace'), ('education', 'education'),
                ('how-To', 'how-to'), ('lifeStyle', 'lifeStyle'), ('gossip', 'gossip'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upload_image = models.ImageField(
        _("Image"), upload_to="profile_images/%Y/%m/", blank=True, null=True)
    image_url = models.CharField(
        max_length=3080, blank=True, null=True)
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
        if self.upload_image:
            self.image_url = f"{MEDIA_URL}{self.upload_image.url}".replace("//", "/")
        if not self.upload_image and not self.image_url:
            self.image_url = f"{STATIC_URL}default_jpg.png"
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        try:
            image_resize(self.upload_image, 144, 144)
        except:
            pass


class Post(models.Model):
    title         = models.CharField(max_length=255, unique=True,
                             help_text="Text limit is 250")
    description   = models.CharField(max_length=200,
                                   help_text="Text limit is 200, and know that this is the post snippet")
    content       = RichTextField()
    author        = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255)
    upload_image  = models.ImageField(_("Image"), upload_to="post_media/image/%Y/%m/", blank=True, null=True)
    image_url     = models.CharField(max_length=3038, null=True, blank=True)
    image_color   = models.CharField(max_length=50, null=True, blank=True)
    image_caption = models.CharField(max_length=100, null=True, blank=True,
                                     help_text="Text limit is 100, and know that this is the post image description")
    video_url     = models.CharField(max_length=3000, null=True, blank=True)
    category      = models.CharField(choices=CategoryList, max_length=50, default='uncategorized')
    hashtags      = TaggableManager(verbose_name=_("Hashtags"))
    likes         = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes      = models.ManyToManyField(User, related_name="dislikes",  blank=True)
    views         = models.IntegerField(default=0, null=True, blank=True)
    scraped       = models.BooleanField(default=False)
    date_posted   = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-id']
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

    @property
    def total_views(self):
        return self.views

    @property
    def total_votes(self):
        return self.votes

    # For Post Detail

    # Without Int
    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    # With Int
    def total_views(self):
        return self.views

    def total_votes(self):
        return self.votes

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('users:post-detail', kwargs={'pk': self.pk})

    def get_api_url(self, request=None):
        api_reverse("post-api:post-api-rud",
                    kwargs={'pk': self.pk}, request=request)

    def save(self, *args, **kwargs):
        if self.upload_image or self.image_url:
            if self.image_url:
                self.image_color = get_image_color(self.image_url, link=True)
            else: 
                self.image_color = get_image_color(self.upload_image)
        if self.upload_image:
            image_url = f"{MEDIA_URL}{self.upload_image.url}".replace("//media", "/")
        if not self.upload_image and not self.image_url:
            self.image_url = f"{STATIC_URL}default.png"
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        if self.upload_image and not self.image_url:
            image_resize(self.upload_image, 800, 600)

        if self.content:
            try:
                self.content = check_for_tag(self.content, Tag)
            except:
                pass


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



@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.upload_image:
        if os.path.isfile(instance.upload_image.path):
            os.remove(instance.upload_image.path)

@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Post` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).upload_image
    except Post.DoesNotExist:
        return False

    new_file = instance.upload_image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)