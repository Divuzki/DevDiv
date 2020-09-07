from django.contrib import admin
from .models import Post, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author'
    ]
    list_display_links = [
        'title'
    ]
    search_fields = [
        'title',
        'author'
    ]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]
    list_display_links = [
        'user'
    ]
    search_fields = [
        'user'
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, UserAdmin)
