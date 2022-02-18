from django.urls import path
from .views import(
    
    # class
    PostListAPI,
    PostCreateAPI,
    PostDetailAPI,

    # func
    api_post_hashtag_view,
    api_latest_post_view,
)

app_name = 'post-api'

urlpatterns = [
    path('', PostListAPI.as_view(), name="post-api-list"),
    path('<int:pk>/', PostDetailAPI.as_view(), name="post-api-rud"),
    path('create-post/', PostCreateAPI.as_view(), name="post-api-create"),

    # hashtag
    path('hashtag/<int:pk>/', api_post_hashtag_view, name="post-hashtag"),

    #latest post
    path('latest/', api_latest_post_view, name="post-api-latest"),
]
