from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductCategoryEditForm
from users.models import User
from products.models import ProductCategory


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


# added methods and class at lesson8
def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    temlate_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)
