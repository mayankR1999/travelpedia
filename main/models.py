from django.db import models
from django.contrib.auth.models import User
import time

# Create your models here.

class Posts(models.Model):
    place = models.CharField(max_length=30)
    experience = models.CharField(max_length=250)
    img = models.ImageField(upload_to = 'pictures')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'user_post_likes')
    total_likes = models.IntegerField(default = 0)
    timestamp = models.CharField(max_length = 25)

    def count_likes(self):
        return self.likes.count()

    def create_timestamp(self):
        self.timestamp = str(time.time())


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_picture = models.ImageField(upload_to='pictures', default='../static/pictures/avatardefault.png')
    user_description = models.CharField(max_length=250, null=True)
    followers = models.ManyToManyField(User, related_name='user_followers')
    following = models.ManyToManyField(User, related_name='user_following')

    def num_of_followers(self):
        return self.followers.count()

    def num_of_following(self):
        return self.following.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    text = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User, related_name = 'comment_likes')
    time_stamp = models.CharField(max_length = 25)

    def count_likes(self):
        return self.likes.count()

    def create_timestamp(self):
        self.time_stamp = str(time.time())