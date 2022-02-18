from django.contrib import admin
from .models import Profile, Category

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

admin.site.register(Profile, UserAdmin)
admin.site.register(Category)
