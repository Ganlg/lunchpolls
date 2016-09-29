from django.contrib import admin
from .models import Post, Restaurant, Vote, Message

# Register your models here.
admin.site.register(Post)
admin.site.register(Restaurant)
admin.site.register(Vote)
admin.site.register(Message)