from django.contrib import admin
from users.models import Post, Comment, HashTag
from .models import PostFlag


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'category',
    ]
    list_display_links = [
        'title',
        'category',
    ]
    search_fields = [
        'title',
        'author__username__icontains',
        'description',
        'hashtag',
        'category',
    ]


class PostFlagAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'post',
        'user'
    ]
    list_display_links = [
        'category'
    ]
    search_fields = [
        'postUUID',
        'post__author__username__icontains',
        'post__description__icontains',
        'category',
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(HashTag)
admin.site.register(PostFlag, PostFlagAdmin)
admin.site.register(Comment)
