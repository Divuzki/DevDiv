from django.urls import path, include, re_path
from .views import (
PostListView, 
PostDetailView,
 PostCreateView,
 PostUpdateView,
 PostDeleteView,
 Profile,
 SearchResultsView,
 UserPostListView
)
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', PostListView.as_view(), name="home"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),

    path('donate/', views.donate, name="donate"),
    path('charge/', views.donate_charge, name="donate_charge"),
    path('success/<str:args>/', views.donate_successMsg, name="donate_success"),

    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(template_name='users/post_update.html'), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),

    path('signup/', views.signup, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="pwdreset"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    

    path('profile/', views.profile, name="profile"),
    path('accounts/profile/', views.profile, name="profile")

]
