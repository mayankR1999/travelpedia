from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Posts
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
        img = request.POST['image']
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


def show_my_posts(request):
    all_posts = Posts.objects.all()
    user = request.user
    my_posts = [post for post in all_posts if post.owner == user]
    
    context = {
        'posts': process_likes(my_posts)
    }
    return render(request, "user-feed.html", context)


def delete_post(request):   # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    post.img.delete()
    post.delete()
    return HttpResponse('')


def process_likes(posts):
    for post in posts:
        post.liked_by = post.likes.all()

    return posts