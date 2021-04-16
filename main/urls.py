from django.urls import path
from . import views

urlpatterns = [
    path('', views.userFeed, name = 'user_feed'),
    path('upload', views.post_upload, name = 'post_upload'),
    path('searchPost', views.searchPost, name = 'searchPost'),
    path('like', views.likePost, name = 'like_post'),
    path('myposts', views.show_my_posts, name = 'show_my_posts'),
    path('deletePost', views.delete_post, name = "delete_post"),
]