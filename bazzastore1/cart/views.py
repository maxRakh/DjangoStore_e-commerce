from django.shortcuts import render, get_object_or_404, redirect
from coupons.forms import CouponApplyForm
from store.models import Product, Category
from .cart import Cart


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

def cart_reduce(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product.id)
    if cart.cart[product_id]['quantity'] == 1:
        cart_remove(request, product_id)
    else:
        cart.add(product=product, reduce=True)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    coupon_apply_form = CouponApplyForm()
    context = {
        'title': 'Корзина покупателя',
        'cart': cart,
        'categories': categories,
        'coupon_apply_form': coupon_apply_form,
    }
    return render(request, 'cart/cart.html', context=context)