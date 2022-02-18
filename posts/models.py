from django.db import models
from users.models import User, Post


FLAG_CHOICES = (
    ('video graphics', 'video graphics'),
    ('Inappropriate', 'Inappropriate'),
    ('Sexual Content', 'Sexual Content'),
)


class PostFlag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postUUID = models.TextField(help_text="Flag UUID")
    category = models.CharField(
        choices=FLAG_CHOICES, max_length=20, default='uncategorized')
    flaged_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category
