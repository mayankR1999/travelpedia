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
