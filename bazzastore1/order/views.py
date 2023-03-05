from django.shortcuts import render
from .models import *
from cart.cart import Cart
from store.models import Category
from .forms import AddOrderForm


def order_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'order/order_complete.html', {'order': order})
    else:
        form = AddOrderForm()

    context = {
        'title': 'Оформление заказа',
        'cart': cart,
        'categories': categories,
        'form': form,
    }
    return render(request, 'order/order.html', context=context)


def order_complete(request):
    categories = Category.objects.all()
    context = {
        'title': 'Заказ оформлен',
        'categories': categories,
    }
    return render(request, 'order/order_complete.html', context=context)
