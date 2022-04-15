from django.db import models

class WebPushNotificationUsers(models.Model):
    registration_id = models.TextField()
    type = models.CharField(max_length=10)
