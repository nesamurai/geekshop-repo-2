from django.urls import path

from . import views


app_name = 'admins'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.admin_users, name='admin_users'),
    path('users-create/', views.admin_users_create, name='admin_users_create'),
    path('users-update/<int:id>/', views.admin_users_update, name='admin_users_update'),
    path('users-delete/<int:id>/', views.admin_users_delete, name='admin_users_delete'),
]
