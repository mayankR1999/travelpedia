from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    place = models.CharField(max_length=30)
    experience = models.CharField(max_length=500)
    img = models.ImageField(upload_to = 'pictures')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
