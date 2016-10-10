from django.contrib import admin
from .models import Post, Restaurant, Vote, Message, Birthday


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'author')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'comment', 'link')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'restaurant', 'rank')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('post', 'user','message', 'timestamp')


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('user', 'month_day')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Birthday, BirthdayAdmin)