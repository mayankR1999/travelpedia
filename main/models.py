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

    def count_comments(self):
        return len(Comment.objects.filter(post=self.id))


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=60)
    display_picture = models.ImageField(upload_to='pictures', default='../static/pictures/avatardefault.png')
    user_description = models.CharField(max_length=250, null=True)
    followers = models.ManyToManyField(User, related_name='user_followers')
    following = models.ManyToManyField(User, related_name='user_following')

    def num_of_followers(self):
        return self.followers.count()

    def num_of_following(self):
        return self.following.count()

    def json(self):
        return {
            'user_id': self.user.id,
            'avatar_url': self.display_picture.url,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    text = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User, related_name = 'comment_likes')
    time_stamp = models.CharField(max_length = 25)

    def count_likes(self):
        return self.likes.count()

    def create_timestamp(self):
        self.time_stamp = str(time.time())

    def time_elapsed(self):
        curr_time = int(time.time())
        elapsed_seconds = curr_time-int(float(self.time_stamp))

        minute, hour, day, week = (60), (60*60), (24*60*60), (7*24*60*60)

        if elapsed_seconds//week >= 1:
            return str(elapsed_seconds//week) + 'w'
        elif elapsed_seconds//day >= 1:
            return str(elapsed_seconds//day) + 'd'
        elif elapsed_seconds//hour >= 1:
            return str(elapsed_seconds//hour) + 'h' 
        elif elapsed_seconds//minute >= 1:
            return str(elapsed_seconds//minute) + 'm'
        else:
            return str(elapsed_seconds) + 's'

    def json(self):
        return {
            'id': self.id,
            'user': {
                'username': self.user.username
            },
            'post': {
                'id': self.post.id
            },
            'user_details': {
                'avatar_url': self.user_details.display_picture.url
            },
            'text': self.text,
            'total_likes': self.count_likes(),
            'liked_by': [user.id for user in self.likes.all()],
            'time_elapsed': self.time_elapsed()
        }