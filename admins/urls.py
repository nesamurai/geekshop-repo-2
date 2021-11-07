from django.urls import path

from . import views


app_name = 'admins'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='admin_users'),
    path('users-create/', views.UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', views.UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', views.UserDeleteView.as_view(), name='admin_users_delete'),
]
