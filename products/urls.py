from django.urls import path

from . import views


app_name = 'products'

urlpatterns = [
    path('', views.products, name='index'),
    path('<int:category_id>/', views.products, name='category'),
    path('page/<int:page>/', views.products, name='page'),
]
