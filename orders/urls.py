from django.urls import path

from orders import views


app_name = 'orders'

urlpatterns = [
    path('', views.OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', views.order_forming_complete, name='order_forming_complete'),
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', views.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', views.OrderUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', views.OrderDelete.as_view(), name='order_delete'),
]
