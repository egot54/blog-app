from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm
from subscriptions.models import Subscription

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'user/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'user/profile.html', {'user': request.user})

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_subscribed = False
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    
    if request.user.is_authenticated and request.user != profile_user:
        is_subscribed = Subscription.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    
    context = {
        'profile_user': profile_user,
        'is_subscribed': is_subscribed,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'user/profile.html', context)