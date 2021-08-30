# Utility functions to make life easier.

from .models import UserDetails
from django.contrib.auth.models import User
from django.db.models import Q
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
        post.total_comments = post.count_comments()
        user_details = UserDetails.objects.get(pk = post.owner)
        post.owner.avatar = user_details.display_picture

    return posts


def search_user_util(query):
    users = UserDetails.objects.filter(Q(username__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query) | Q(full_name__icontains = query))

    sorting_util_list = [[user, 0] for user in users]
    for i in range(len(users)):
        if query not in users[i].username:
            sorting_util_list[i][1] += 5
            if query in users[i].first_name:
                sorting_util_list[i][1] += (len(users[i].first_name) - 1)
            if query in users[i].last_name:
                sorting_util_list[i][1] += (len(users[i].last_name) - 1)
            if query in users[i].full_name:
                sorting_util_list[i][1] -= 1
        else:
            sorting_util_list[i][1] += len(users[i].username)
            if not users[i].username.startswith(query):
                sorting_util_list[i][1] += 1
        if not users[i].first_name.startswith(query):
            sorting_util_list[i][1] += 1
        if not users[i].last_name.startswith(query):
            sorting_util_list[i][1] += 1
        if not users[i].full_name.startswith(query):
            sorting_util_list[i][1] += 1

    sorted_util_list = sorted(sorting_util_list, key=itemgetter(1))
    
    sorted_users = [user[0] for user in sorted_util_list]

    return sorted_users