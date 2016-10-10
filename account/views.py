from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ChangePassword, EditProfileForm
from django.contrib import messages
from lunch.models import Birthday



# Create your views here.
def user_login(request):
    next_page = '/'
    if request.method == 'GET':
        next_page = request.GET['next']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST['next']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_page)
    return render(request, 'account/login.html', {'next': next_page})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            birth_date = register_form.cleaned_data['birth_date']
            Birthday.objects.create(user=new_user, birth_date=birth_date)
            login(request, new_user)
            return redirect('/')
    else:
        register_form = RegisterForm(None)
    return render(request, 'account/register.html', {'form': register_form})

@login_required
def user_change_password(request):
    form = ChangePassword(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            if request.user.check_password(cd['current_password']):
                request.user.set_password(cd['new_password'])
                return redirect(reverse('account'))
            else:
                messages.error(request, 'Incorrect Password')

    return render(request, 'account/change_password.html', {'form': form })

@login_required
def index(request):
    return render(request, 'account/index.html')

@login_required
def edit_profile(request):
    user = request.user
    try:
        birthday = Birthday.objects.get(user=user)
    except:
        birthday = None

    form = EditProfileForm(initial={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birthday': birthday.birth_date if birthday else None
    })
    if request.POST:
        form = EditProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()

            if birthday is None:
                Birthday.objects.create(user=user, birth_date=cd['birthday'])
            else:
                birthday.birth_date = cd['birthday']
                birthday.save()

            return redirect(reverse('account:index'))
    return render(request, 'account/edit_profile.html', {'form': form})

