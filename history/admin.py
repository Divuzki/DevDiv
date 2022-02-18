from django.contrib import admin
from .models import History


class HistoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'content_type',
        'viewed_on'
    ]
    list_display_links = [
        'user'
    ]
    search_fields = [
        'user',
        'content_object',
        'object_id'
    ]


admin.site.register(History, HistoryAdmin)
