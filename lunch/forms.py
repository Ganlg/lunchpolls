from django import forms
from .models import Post, Restaurant
# from datetimewidget.widgets import DateTimeWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'comment', 'time', 'status']
        # widgets ={
        #     'time': DateTimeWidget(usel10n=True, bootstrap_version=3)
        # }

class RestForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant', 'link']




