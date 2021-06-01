# Utility functions to make life easier.

from .models import UserDetails
from django.contrib.auth.models import User
from operator import itemgetter

# Utility function to get details of users like username and avatar.
def getOverviewDetails(users):
    overview_arr = sorted([[user, user.first_name + ' ' + user.last_name] for user in users], key = itemgetter(1))

    for i in range(len(overview_arr)):
        user_details = UserDetails.objects.get(pk = overview_arr[i][0])
        overview_arr[i] = (overview_arr[i][0], user_details.display_picture)

    return overview_arr


# Function to add the IDs of users (who liked the post) to post details.
def process_likes_and_avatars(posts):
    for post in posts:
        post.liked_by = post.likes.all()
        user_details = UserDetails.objects.get(pk = post.owner)
        post.owner.avatar = user_details.display_picture

    return posts