from django.urls import path
from . import views

urlpatterns = [
    path('', views.userFeed, name = 'user_feed'),
    path('upload', views.post_upload, name = 'post_upload'),
    path('searchPost', views.searchPost, name = 'searchPost'),
    path('like', views.likePost, name = 'like_post'),
    path('profile/<int:id>', views.show_user_profile, name = 'show_user_profile'),
    path('profile/changeDP', views.change_dp, name = 'change_dp'),
    path('profile/removeDP', views.remove_dp, name = 'remove_dp'),
    path('profile/changeBio', views.change_bio, name = 'change_bio'),
    path('deletePost', views.delete_post, name = "delete_post"),
]