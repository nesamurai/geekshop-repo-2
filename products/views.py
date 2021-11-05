from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from products.models import Product, ProductCategory


def index(request):
    title = 'GeekShop'
    return render(request, 'products/index.html', {'title': title})

def products(request, category_id=None, page=1):
    title = 'GeekShop - Каталог'
    categories = ProductCategory.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    return render(request, 'products/products.html', {'title': title,
                                                        'products': products_paginator,
                                                        'categories': categories})
