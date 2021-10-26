from django.urls import path

from . import views


app_name = 'baskets'

urlpatterns = [
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:id>/', views.basket_remove, name='basket_remove'),
]
