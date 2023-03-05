from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from cart.cart import Cart
from .models import *


# from bazzastore1.store.models import Product


def store(request, category_slug=None):
    category = None
    cart = Cart(request)
    categories = Category.objects.all()
    products = Product.objects.filter(is_published=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'title': 'Интернет магазин MAZZA.BAGAM',
        'products': products,
        'category': category,
        'categories': categories,
        'cart': cart,
    }

    return render(request, 'store/store.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_published=True)
    categories = Category.objects.all()
    cart = Cart(request)
    context = {
        'title': product.title,
        'product': product,
        'category': product.category,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'store/detail.html', context=context)


# Реализуем это  вместо функции позже и отладим
# class Store(ListView):
#     product = Product
#     template_name = 'store/store.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
