from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
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
    key = request.POST['searchKey']
    filtered_posts = Posts.objects.filter(place__contains=key)
    context = {
        'posts' : filtered_posts
    }
    return render(request, "base.html", context)