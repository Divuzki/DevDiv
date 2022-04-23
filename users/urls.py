from django.urls import path
from . import views
from history.views import HistoryList, HistoryDelete
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', views.PostListView.as_view(), name="home"),
    path('user/post/history/', HistoryList.as_view(), name='history'),
    path('user/history/delete/<int:pk>/',
         HistoryDelete.as_view(), name='history_del'),

    path('post/flag/<int:pk>/', views.post_flag_view, name="flag"),
    path('post/flagging/<str:postuuid>/',
         views.post_flagging_view, name="flagging"),

    # Api
    path("post/comment/create/<int:pk>/",
         views.comment_create_view, name="create-comment"),
    path("post/comment/list/<str:post>/",
         views.comment_list_view, name="list-comment"),
    path('user/<str:username>', views.UserPostListView.as_view(), name="user-posts"),

    path('donate/', views.donate, name="donate"),
    path('charge/', views.donate_charge, name="donate_charge"),
    path('success/<str:args>/', views.donate_successMsg, name="donate_success"),

    path('post/<int:pk>/', views.post_detail, name="post-detail"),

    # Auth
    path('signup/', views.signup, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name="pwdreset"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),

    path('profile/update', views.profile_update_view, name="profile-update"),

    path('post/<int:pk>/update/', views.PostUpdateView.as_view(
        template_name='users/post_update.html'), name="post-update"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post-delete"),
    path('post/new/', views.PostCreateView.as_view(), name="post-create"),


    path('hashtag/', views.hashtag_autocomplete, name="autocomplete"),
    path('hashtag/<str:tag_qs>', views.hashtag_view, name="hashtag"),
    path('profile/', views.profile, name="profile"),
    path('category/<str:cats>', views.category_view, name='category'),
    path('post/like/<int:pk>', views.LikeView, name="like_post"),
    path('post/dislike/<int:pk>', views.DislikeView, name="dislike_post"),
    path('search/', views.search_result_view, name="search"),
    path('t', views.test, name="test"),

]
