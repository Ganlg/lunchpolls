from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import Post, Restaurant, Vote
from .forms import PostForm, RestForm
from django.db.models import Avg



# Create your views here.
def index(request, tab=None):
    tab = tab or '1'
    args = {
        'posts': None,
        'tab': tab
    }
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(author=request.user)
        user_published = Post.published.filter(author=request.user)
        user_drafts = Post.drafted.filter(author=request.user)
        if tab == '2':
            args['posts'] = user_posts
        elif tab == '3':
            args['posts'] = user_published
        elif tab == '4':
            args['posts'] = user_drafts
        else:
            published = Post.published.all()
            args['posts'] = published
    else:
        published = Post.published.all()
        args['posts'] = published

    return render(request, 'lunch/index.html', args)

@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            import random
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title + " " + timezone.now().strftime('%B %d, %Y, %I:%M %p') + str(random.randint(0,100)))
            new_post.author = request.user
            new_post.save()
            return redirect('/')

    return render(request, 'lunch/create_post.html', {'form': form})

@login_required
def add_restaurant(request):
    form = RestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_rest = form.save()
            return redirect(reverse('lunch:view_restaurant'))
    return render(request, 'lunch/add_restaurant.html', {'form': form})


def view_restaurant(request):
    rest = Restaurant.objects.all()
    return render(request, 'lunch/view_restaurants.html', {'restaurants': rest})

@login_required
def delete_restaurant(request, pk):
    if request.user.is_staff:
        rest = Restaurant.objects.get(pk=pk)
        rest.delete()
    return redirect(reverse("lunch:view_restaurant"))

@login_required
def edit_restaurant(request, pk):
    rest = Restaurant.objects.get(pk=pk)
    form = RestForm(instance=rest)
    if request.user.is_staff:
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect(reverse("lunch:view_restaurant"))
    return render(request, 'lunch/edit_restaurant.html', {'form': form})

@login_required
def detail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    restaurants = Restaurant.objects.all()
    voted = len(Vote.objects.filter(post=post, user=request.user)) > 0 or post.time < timezone.now()

    if request.method == 'POST' and not voted:
        r1 = get_object_or_404(Restaurant, pk=request.POST['first'])
        r2 = get_object_or_404(Restaurant, pk=request.POST['second'])
        r3 = get_object_or_404(Restaurant, pk=request.POST['third'])

        for i, rest in enumerate([r1, r2, r3]):
            vote = Vote(user=request.user, restaurant=rest, post=post, rank=3-i)
            vote.save()
        post.votes += 1
        post.save()
        return redirect(reverse('lunch:detail_post', args=[slug]))

    vote_detail = None
    top1 = 'Not Voted'
    top2 = 'Not Voted'
    score1 = 0
    score2 = 0
    if voted:
        vote_detail = Vote.objects.filter(post=post).order_by('user', '-rank')
        top_list = list(post.vote_set.values('restaurant').annotate(score=Avg('rank')).order_by('-score')[0:2])

        if len(top_list) > 0:
            top1, top2 = [Restaurant.objects.get(pk=x['restaurant']).restaurant for x in top_list ]
            score1, score2 = [x['score'] for x in top_list]


    return render(request, 'lunch/detail_post.html', {
        'post': post,
        'restaurants': restaurants,
        'voted': voted,
        'vote_detail': vote_detail,
        'top1': top1,
        'top2': top2,
        'score1': score1,
        'score2': score2
    })

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author or request.user.is_staff:
        post.delete()
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
        return redirect(referer)
    return redirect(reverse("lunch:index"))

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        new_form = PostForm(request.POST)
        if new_form.is_valid():
            cd = new_form.cleaned_data
            post.title = cd['title']
            post.comment = cd['comment']
            post.time = cd['time']
            post.status = cd['status']
            post.save()
            # if 'HTTP_REFERER' in request.META:
            #     referer = request.META['HTTP_REFERER']
            #     return redirect(referer)
            # else:
            return redirect(reverse('lunch:index'))
    return render(request, 'lunch/edit_post.html', {'form': form, 'slug': slug})