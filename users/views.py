from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from . import forms


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
            print(form.errors)
    else:
        form = forms.UserLoginForm()
    title = 'GeekShop - Авторизация'
    return render(request, 'users/login.html', {'title': title, 'form': form})

def registration(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = forms.UserRegistrationForm()
    title = 'GeekShop - Регистрация'
    return render(request, 'users/registration.html', {'title': title, 'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
