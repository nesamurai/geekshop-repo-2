from django.shortcuts import render

from products.models import Product, ProductCategory


def index(request):
    title = 'GeekShop'
    return render(request, 'products/index.html', {'title': title})

def products(request):
    title = 'GeekShop - Каталог'
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    return render(request, 'products/products.html', {'title': title, 'products': products,
                                                                    'categories': categories})
