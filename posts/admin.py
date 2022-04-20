from django.contrib import admin
from users.models import Post, Comment, HashTag
from .models import PostFlag
from .custom_actions import (apply_foreign, apply_local, apply_sports, apply_politics, apply_technology,
                             apply_science, apply_how_To, apply_finace, apply_lifeStyle, apply_education, apply_gossip)


apply_local.short_description = 'Local As Category'
apply_sports.short_description = 'Sports As Category'
apply_politics.short_description = 'Politics As Category'
apply_technology.short_description = 'Technology As Category'
apply_science.short_description = 'Science As Category'
apply_how_To.short_description = 'How-To As Category'
apply_finace.short_description = 'Finace As Category'
apply_lifeStyle.short_description = 'LifeStyle As Category'
apply_education.short_description = 'Education As Category'
apply_gossip.short_description = 'Gossip As Category'
apply_foreign.short_description = 'Foreign As Category'


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
        'author__username',
        'description',
        'hashtag__name',
        'category',
    ]
    actions = [apply_foreign, apply_local, apply_sports, apply_politics, apply_technology, apply_science, apply_how_To,
               apply_finace, apply_lifeStyle, apply_education, apply_gossip]  # <-- Add the list action function here


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
        'post__author__username',
        'post__description',
        'category',
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(HashTag)
admin.site.register(PostFlag, PostFlagAdmin)
admin.site.register(Comment)
