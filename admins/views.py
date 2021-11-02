from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from users.models import User


@user_passes_test(lambda u: u.is_staff)
def index(request):
    title = 'GeekShop - Админ-панель'
    return render(request, 'admins/index.html', {'title': title})

# Create
@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    title = 'GeekShop - Создание пользователей'
    return render(request, 'admins/admin-users-create.html', {'title': title, 'form': form})

# Read
@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    title = 'GeekShop - Пользователи'
    users = User.objects.all()
    return render(request, 'admins/admin-users-read.html', {'title': title, 'users': users})

# Update
@user_passes_test(lambda u: u.is_staff)
def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    title = 'GeekShop - Обновление пользователя'
    return render(request, 'admins/admin-users-update-delete.html', {'title': title, 'form': form, 'selected_user': selected_user})

# Delete
@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_users'))
