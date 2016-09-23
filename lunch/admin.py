from django.contrib import admin
from .models import Post, Restaurant, Vote

# Register your models here.
admin.site.register(Post)
admin.site.register(Restaurant)
admin.site.register(Vote)