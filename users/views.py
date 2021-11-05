from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from . import forms
from baskets.models import Basket
from users.models import User


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
            user = form.save()
            if send_confirmation_mail(user):
                messages.success(request, "На ваш почтовый ящик отправлено письмо о подтверждении создания учетной записи")
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.error(request, "Ошибка при отправке письма")
                return HttpResponseRedirect(reverse('users:login'))
    else:
        form = forms.UserRegistrationForm()
    title = 'GeekShop - Регистрация'
    return render(request, 'users/registration.html', {'title': title, 'form': form})


@login_required
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


def send_confirmation_mail(user):
    confirmation_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение создания учетной записи для {user.username}'
    message = f'Для подтверждения создания учетной записи для {user.username} на портале'\
    f' {settings.DOMAIN_NAME} перейдите по ссылке {settings.DOMAIN_NAME}{confirmation_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verification(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'users/verification.html')
        else:
            messages.error(request, "Ошибка при активации пользователя")
            return render(request, 'users/verification.html')
    except Exception as e:
        print(f'activation error: {e.args}')
        return HttpResponseRedirect(reverse('index'))
