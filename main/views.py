from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Posts
from . import forms

# Create your views here.

def home(request):
    return render(request, "home.html")


def custom_user(request):
    all_posts = Posts.objects.all()
    context = {
        'posts': all_posts
    }
    return render(request, "base.html", context)


def post_upload(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.owner = request.user
            instance.save()
            return redirect('../../accounts/base/')
    else:
        form = forms.CreatePost()
        context = {
            'form':form
        }
        return render(request, "upload.html", context)


def searchPost(request):
    key = request.POST['searchKey'].lower()
    all_posts = Posts.objects.all()
    filtered_posts = [post for post in all_posts if post.place.lower() == key]

    context = {
        'posts' : filtered_posts
    }
    return render(request, "base.html", context)


def likePost(request):      # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    user = request.user
    if user not in post.likes.all():
        post.likes.add(user)
    else:
        post.likes.remove(user)
    post.total_likes = post.count_likes()
    post.save()
    return HttpResponse(str(post.total_likes))


def show_my_posts(request):
    all_posts = Posts.objects.all()
    user = request.user
    my_posts = [post for post in all_posts if post.owner == user]
    
    context = {
        'posts': my_posts
    }
    return render(request, "base.html", context)

def delete_post(request):   # Use AJAX
    post = Posts.objects.get(id = request.GET['post_id'])
    post.delete()
    return HttpResponse('')