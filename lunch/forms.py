from django import forms
from .models import Post, Restaurant


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'comment', 'time', 'status']


class RestForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant', 'link']




