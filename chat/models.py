from django.db import models
from lunch.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("timestamp",)