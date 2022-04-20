from users.models import Post
# Categories Custom Action Button For Posts Query :)


def apply_foreign(self, request, queryset):
    posts = []
    for post in queryset:
        post.category = "foreign"
        post.save()


def apply_local(self, request, queryset):
    for post in queryset:
        post.category = "local"
        post.save()


def apply_sports(self, request, queryset):
    for post in queryset:
        post.category = "sports"
        post.save()


def apply_politics(self, request, queryset):
    for post in queryset:
        post.category = "politics"
        post.save()


def apply_technology(self, request, queryset):
    for post in queryset:
        post.category = "technology"
        post.save()


def apply_science(self, request, queryset):
    for post in queryset:
        post.category = "science"
        post.save()


def apply_how_To(self, request, queryset):
    for post in queryset:
        post.category = "how-To"
        post.save()


def apply_finace(self, request, queryset):
    for post in queryset:
        post.category = "finace"
        post.save()


def apply_lifeStyle(self, request, queryset):
    for post in queryset:
        post.category = "lifeStyle"
        post.save()


def apply_education(self, request, queryset):
    for post in queryset:
        post.category = "education"
        post.save()


def apply_gossip(self, request, queryset):
    for post in queryset:
        post.category = "gossip"
        post.save()
