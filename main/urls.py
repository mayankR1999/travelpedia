from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('accounts/base/', views.custom_user, name = 'custom_user'),
    path('accounts/base/upload', views.post_upload, name = 'post_upload'),
    path('accounts/base/searchPost', views.searchPost, name = 'searchPost'),
    path('accounts/base/like', views.likePost, name = 'like_post'),
    path('accounts/base/myposts', views.show_my_posts, name = 'show_my_posts'),
    path('accounts/base/deletePost', views.delete_post, name = "delete_post"),
]