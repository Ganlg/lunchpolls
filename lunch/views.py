from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import Post, Restaurant, Vote
from .forms import PostForm, RestForm
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from chat.models import Message


# Create your views here.
def index(request, tab=None):
    tab = tab or '1'
    args = {
        'posts': None,
        'tab': tab
    }
    object_list = None

    if request.user.is_authenticated:
        if tab == '2':
            object_list = Post.objects.filter(author=request.user)
        elif tab == '3':
            object_list = Post.published.filter(author=request.user)

        elif tab == '4':
            object_list = Post.drafted.filter(author=request.user)

        else:
            object_list = Post.published.all()

    else:
        object_list = Post.published.all()

    page = request.GET.get('page')
    num_pg = 20
    paginator = Paginator(object_list, num_pg)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    args['posts'] = posts
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
    object_list = Restaurant.objects.all()
    num_pg = 20
    paginator = Paginator(object_list, num_pg)
    page = request.GET.get('page')
    try:
        rest = paginator.page(page)
    except PageNotAnInteger:
        rest = paginator.page(1)
    except EmptyPage:
        rest = paginator.page(paginator.num_pages)

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

    if request.user.is_staff:
        if request.POST:
            new_form = RestForm(request.POST, instance=rest)
            if new_form.is_valid():
                new_form.save()
                return redirect(reverse("lunch:view_restaurant"))
    form = RestForm(instance=rest)
    return render(request, 'lunch/edit_restaurant.html', {'form': form})

@login_required
def detail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    restaurants = Restaurant.objects.all()
    voted = len(Vote.objects.filter(post=post, user=request.user)) > 0 or post.time < timezone.now()
    comments = Message.objects.filter(post=post)

    if request.method == 'POST' and not voted:
        r1 = get_object_or_404(Restaurant, pk=request.POST['first'])
        r2 = get_object_or_404(Restaurant, pk=request.POST['second'])
        r3 = get_object_or_404(Restaurant, pk=request.POST['third'])
        ex = get_object_or_404(Restaurant, pk=request.POST['exclude'])
        if not(r1.pk in [r2.pk, r3.pk, ex.pk] or r2.pk in [r1.pk, r3.pk, ex.pk]
               or r3.pk in [r1.pk, r2.pk, ex.pk] or ex.pk in [r1.pk, r2.pk, r3.pk]):
            for i, rest in enumerate([r1, r2, r3, ex]):
                rank = 3 - i
                if i == 3:
                    rank = -3
                vote = Vote(user=request.user, restaurant=rest, post=post, rank=rank)
                vote.save()

            post.votes += 1
            post.save()
            return redirect(reverse('lunch:detail_post', args=[slug]))
        else:
            messages.error(request, 'Your choices have to be different!')

    vote_detail = None
    top1 = 'Not Voted'
    top2 = 'Not Voted'
    score1 = 0
    score2 = 0
    if voted:
        vote_detail = Vote.objects.filter(post=post).order_by('user', '-rank')
        top_list = list(post.vote_set.values('restaurant').annotate(score=Sum('rank')).order_by('-score')[0:2])

        if len(top_list) > 0:
            top1, top2 = [Restaurant.objects.get(pk=x['restaurant']).restaurant for x in top_list ]
            score1, score2 = ["%.1f" % (x['score']/post.votes) for x in top_list]


    return render(request, 'lunch/detail_post.html', {
        'post': post,
        'restaurants': restaurants,
        'voted': voted,
        'vote_detail': vote_detail,
        'top1': top1,
        'top2': top2,
        'score1': score1,
        'score2': score2,
        'comments': comments
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