from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ChangePassword
from django.contrib import messages


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return redirect('/')


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
