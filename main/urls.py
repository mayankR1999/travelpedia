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
    path('follow_toggle', views.follow_toggle, name = "follow_toggle_request"),
    path('remove_follower', views.remove_follower, name = "remove_follower"),
    path('explore', views.explore, name = "explore"),
    path('submitNewComment', views.add_comment, name = "add_comment"),
    path('loadComments', views.load_comments, name = "load_comments"),
    path('likeComment', views.like_comment, name = "like_comment"),
    path('getPostDetails', views.get_post_details, name = "get_post_details"),
    path('searchUser', views.search_user, name = "search_user"),
]