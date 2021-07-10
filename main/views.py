from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Posts, UserDetails
from .functions import *
import os

# Create your views here.

def userFeed(request):
    all_posts = Posts.objects.all()
    user_details = UserDetails.objects.get(pk = request.user)
    
    context = {
        'posts': process_likes_and_avatars(all_posts),
        'info': {
            'followers': user_details.followers.all(),
            'following': user_details.following.all()
        },
        'avatar': user_details.display_picture
    }
    return render(request, "user-feed.html", context)


def post_upload(request):
    if request.method == "POST":
        place = request.POST['place']
        description = request.POST['exp']
        img = request.FILES['image']

        new_post = Posts(place = place, experience = description, img = img, owner = request.user)
        new_post.create_timestamp()
        new_post.save()
        
        return redirect('../user')
    else:
        return render(request, "upload.html", {'avatar': UserDetails.objects.get(pk = request.user).display_picture})


def searchPost(request):
    key = request.POST['searchKey'].lower()
    all_posts = Posts.objects.all()
    filtered_posts = [post for post in all_posts if post.place.lower() == key]

    context = {
        'posts' : process_likes_and_avatars(filtered_posts)
    }
    return render(request, "user-feed.html", context)


def likePost(request):      # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    user = request.user
    if user not in post.likes.all():
        post.likes.add(user)
    else:
        post.likes.remove(user)
    post.total_likes = post.count_likes()
    post.save()

    context = {
        'numberoflikes': post.total_likes
    }
    return JsonResponse(context)


def show_user_profile(request, id):
    user = User.objects.get(id = id)
    user_posts = Posts.objects.filter(owner = user)
    user_details = UserDetails.objects.get(pk = user)

    context = {
        'posts': process_likes_and_avatars(user_posts),
        'info': {
            'user': user_details.user,
            'dp': user_details.display_picture,
            'user_description': user_details.user_description,
            'followers': getOverviewDetails(user_details.followers.all()),
            'following': getOverviewDetails(user_details.following.all())
        },
        'avatar': user_details.display_picture
    }
    
    return render(request, "user-profile.html", context)


def delete_post(request):   # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    post.img.delete()
    post.delete()
    return HttpResponse('')


def change_dp(request):
    newDP = request.FILES['pic']
    user = request.user
    user_details = UserDetails.objects.get(user = user)
    
    if "avatardefault" not in user_details.display_picture.url:
        user_details.display_picture.delete()
    user_details.display_picture = newDP
    user_details.save()

    url = '../profile/{}'.format(user.id)
    return HttpResponseRedirect(url)


def remove_dp(request):
    user = request.user
    user_details = UserDetails.objects.get(user = user)
    default_user_details = UserDetails.objects.get(user__username = 'default')

    if "avatardefault" not in user_details.display_picture.url:
        user_details.display_picture.delete()
        user_details.display_picture = default_user_details.display_picture
    user_details.save()

    return HttpResponse()


def change_bio(request):
    bio = request.POST['text']
    user = request.user
    user_details = UserDetails.objects.get(user = user)

    user_details.user_description = bio
    user_details.save()

    return HttpResponse()


def follow_toggle(request):
    user1, user2 = request.user, request.GET['user_id']
    request_type = request.GET['request_type']
    user1_details = UserDetails.objects.get(pk = user1)
    user2_details = UserDetails.objects.get(pk = user2)
    if request_type == 'follow':
        user1_details.following.add(user2)
        user2_details.followers.add(user1)
    else:
        user1_details.following.remove(user2)
        user2_details.followers.remove(user1)
    return HttpResponse()


def remove_follower(request):
    user1, user2 = request.user, request.GET['user_id']
    user1_details = UserDetails.objects.get(pk = user1)
    user2_details = UserDetails.objects.get(pk = user2)

    user1_details.followers.remove(user2)
    user2_details.following.remove(user1)
    return HttpResponse()


def explore(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'explore.html')