from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .signals import object_viewed_signal
User = settings.AUTH_USER_MODEL

# User History


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)  # Post
    object_id = models.PositiveIntegerField()  # pk or id
    content_object = GenericForeignKey()  # the content
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_type)

    class Meta:
        verbose_name_plural = "User Histories"


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    qs = History.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(sender), object_id=instance.pk).first()
    if qs is None:
        History.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.pk
        )


object_viewed_signal.connect(object_viewed_receiver)
