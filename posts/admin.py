from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from users.models import Post, Comment, HashTag
from .models import PostFlag


class PostAdmin(admin.ModelAdmin):
    actions = ['update_category']

    def update_category(self, request, queryset):
        # All requests here will actually be of type POST
        # so we will need to check for our special key 'apply'
        # rather than the actual request type
        if 'apply' in request.POST:
            # The user clicked submit on the intermediate form.
            # Perform our update action:
            queryset.update(category=request.POST["category"])

            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            self.message_user(request,
                              "Changed Category on {} posts".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'admin/post_intermediate.html',
                      context={'posts': queryset})

    update_category.short_description = "Update Category"

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
