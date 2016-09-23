from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Restaurant(models.Model):
    restaurant = models.CharField(max_length=250, null=False, blank=False, unique=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('restaurant',)

    def __str__(self):
        return self.restaurant


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField(null=False, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='published')

    restaurants = models.ManyToManyField(Restaurant, through='Vote', through_fields=('post', 'restaurant'))

    votes = models.IntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()
    drafted = DraftManager()

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rank = models.IntegerField()
