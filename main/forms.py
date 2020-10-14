from django import forms
from .import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields = ['place', 'experience', 'img']