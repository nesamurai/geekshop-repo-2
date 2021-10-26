from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from . import forms
from baskets.models import Basket


def login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = forms.UserLoginForm()
    title = 'GeekShop - Авторизация'
    return render(request, 'users/login.html', {'title': title, 'form': form})


def registration(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Вы успешно зарегистрировались!")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = forms.UserRegistrationForm()
    title = 'GeekShop - Регистрация'
    return render(request, 'users/registration.html', {'title': title, 'form': form})


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = forms.UserProfileForm(instance=user)
    title = 'GeekShop - Профиль'
    baskets = Basket.objects.filter(user=user)
    return render(request, 'users/profile.html', {'title': title, 'form': form, 'baskets': baskets})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
