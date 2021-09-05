from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Posts, UserDetails, Comment
from django.core import serializers
from .functions import *
from PIL import Image
import os, json

# Create your views here.

def userFeed(request):
    all_posts = Posts.objects.all()
    user_details = UserDetails.objects.get(pk = request.user)
    
    context = {
        'is_profile_page': False,
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
    user_being_visited = User.objects.get(id = id)
    user_being_visited_posts = Posts.objects.filter(owner =user_being_visited)
    user_being_visited_details = UserDetails.objects.get(pk = user_being_visited)

    logged_user_details = UserDetails.objects.get(pk = request.user)

    context = {
        'is_profile_page': True,
        'posts': process_likes_and_avatars(user_being_visited_posts),
        'info': {
            'user': user_being_visited_details.user,
            'dp': user_being_visited_details.display_picture,     # avatar of user whose profile is being viewed
            'user_description': user_being_visited_details.user_description,
            'followers': getOverviewDetails(user_being_visited_details.followers.all()),
            'following': getOverviewDetails(user_being_visited_details.following.all())
        },
        'avatar': logged_user_details.display_picture,      # avatar of user logged in
        'logged_user_followings': logged_user_details.following.all(),
        'logged_user_followers': logged_user_details.followers.all()
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
        logged_user_details = UserDetails.objects.get(pk = request.user)
        accounts = list(UserDetails.objects.all())

        context = {
            'posts': Posts.objects.all(),
            'initial_accounts': accounts[:4],
            'hidden_accounts': accounts[4:],
            'logged_user_followers': [acc.id for acc in logged_user_details.followers.all()],
            'logged_user_following': [acc.id for acc in logged_user_details.following.all()]
        }

        return render(request, 'explore.html', context)


def get_post_details(request):
    postID = request.GET['postID']
    post = Posts.objects.get(id = postID)
    user_details = UserDetails.objects.get(pk = post.owner)

    width, height = Image.open(post.img).size

    context = {
        'post': {
            'liked': True if request.user in post.likes.all() else False,
            'img': {
                'url': post.img.url,
                'width': width,
                'height': height
            },
            'owner':{
                'id': post.owner.id,
                'username': post.owner.username,
                'avatar': user_details.display_picture.url
            }
        }
    }

    return HttpResponse(json.dumps(context))


def search_user(request):
    search_query = request.POST['search_query']
    logged_user_details = UserDetails.objects.get(pk = request.user)

    queried_user_details = search_user_util(search_query)
    data = [user_detail.json() for user_detail in queried_user_details]
    context = {
        'initial_accounts': data[:4],
        'hidden_accounts': data[4:]
    }

    return HttpResponse(json.dumps(context))
    

def add_comment(request):
    postID = request.POST['postID']
    comment_text = request.POST['comment_text']

    new_comment = Comment(user = request.user, post = Posts.objects.get(id = postID), 
                        user_details = UserDetails.objects.get(pk = request.user) ,text = comment_text)
    new_comment.create_timestamp()
    new_comment.save()

    return HttpResponse(str(Posts.objects.get(id=postID).count_comments()))


def load_comments(request):
    postID = request.GET['postID']
    comments = Comment.objects.filter(post = postID)
    for comment in comments:
        likes = comment.count_likes()
        comment.total_likes = likes

    data = [comment.json() for comment in comments]

    return HttpResponse(json.dumps(data))


def like_comment(request):
    commentID = request.GET['commentID']
    user = request.user
    comment = Comment.objects.get(id=commentID)

    context = {}
    if user not in comment.likes.all():
        comment.likes.add(user)
        context['action'] = 'liked'
    else:
        comment.likes.remove(user)
        context['action'] = 'disliked'

    context['total_likes'] = comment.count_likes()
    comment.save()

    return HttpResponse(json.dumps(context))