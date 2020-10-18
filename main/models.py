from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    place = models.CharField(max_length=30)
    experience = models.CharField(max_length=500)
    img = models.ImageField(upload_to = 'pictures')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'user_post_likes')
    total_likes = models.IntegerField(default = 0)

    def count_likes(self):
        return self.likes.count()
