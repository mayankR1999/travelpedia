from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Posts, UserDetails
import os

# Create your views here.

def userFeed(request):
    all_posts = Posts.objects.all()
    
    context = {
        'posts': process_likes(all_posts)
    }
    return render(request, "user-feed.html", context)


def post_upload(request):
    if request.method == "POST":
        place = request.POST['place']
        description = request.POST['exp']
        img = request.FILES['image']
        new_post = Posts(place = place, experience = description, img = img)
        new_post.save()
        return redirect('../../accounts/base/')
    else:
        
        return render(request, "upload.html")


def searchPost(request):
    key = request.POST['searchKey'].lower()
    all_posts = Posts.objects.all()
    filtered_posts = [post for post in all_posts if post.place.lower() == key]

    context = {
        'posts' : process_likes(filtered_posts)
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
        'posts': process_likes(user_posts),
        'info': {
            'user': user_details.user,
            'dp': user_details.display_picture,
            'user_description': user_details.user_description,
            'followers': user_details.followers.all(),
            'following': user_details.following.all()
        }
    }
    
    return render(request, "user-profile.html", context)


def delete_post(request):   # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    post.img.delete()
    post.delete()
    return HttpResponse('')


def process_likes(posts):
    for post in posts:
        post.liked_by = post.likes.all()

    return posts


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