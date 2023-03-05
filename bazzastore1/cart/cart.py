from decimal import Decimal

from django.conf import settings
from coupons.models import Coupon
from store.models import Product


class Cart(object):
    """Класс корзины"""
    def __init__(self, request):
        """Инициаизацця корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняется пустая корзина в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохранение текущего примененного купона в сессии
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, reduce=False):
        """Добавляем или убавляем товар в корзине"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if not reduce:
            self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def __iter__(self):
        """Перебираем товары в корзине и получаем товары из базы данных"""
        product_ids = self.cart.keys()
        # Получаем товары и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Считаем сколько товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """Сохраняем товар"""
        self.session.modified = True

    def remove(self, product):
        """Удаляем товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Получаем общую стоимость"""
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищаем корзину в текущей сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """Пытаемся получить объект купона по coupon_id из сессии"""
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)

    def get_discount(self):
        """Получаем размер скидки на текущую корзину по данному купону"""
        if self.coupon:
            return int((self.coupon.discount / Decimal('100')) * self.get_total_price())
        return Decimal('0')

    def get_total_price_after_coupon(self):
        """Получаем стоиомость корзины после применения купона"""
        return self.get_total_price() - self.get_discount()