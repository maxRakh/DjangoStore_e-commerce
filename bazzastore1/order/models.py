from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.models import Coupon
from store.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия покупателя')
    phohe_number = models.CharField(max_length=20, verbose_name='Телефон покупателя')
    email = models.EmailField(verbose_name='Email')
    types_of_connect = [
        ('WhatsApp', 'WhatsApp'),
        ('Telegram', 'Telegram'),
        ('Email', 'Email'),
    ]
    type_of_connection = models.CharField(max_length=100, choices=types_of_connect,
                                          verbose_name='Как с вами связаться')
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    address = models.CharField(max_length=255, verbose_name='Улица, дом и др.')
    city = models.CharField(max_length=255, verbose_name='Город')
    country = models.CharField(max_length=255, default='Российская Федерация', verbose_name='Страна')
    extra = models.CharField(max_length=500, null=True, verbose_name='Дополнительно')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Промокод')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Размер скидки %')

    class Meta:
        ordering = ('-date_ordered',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order {self.pk}"

    def get_total_coast(self):
        total_coast = sum(item.get_cost() for item in self.items.all())
        return total_coast - int(total_coast * (self.discount / Decimal('100')))

    get_total_coast.__name__ = 'Стоимость заказа'

    def get_order_list(self):
        return ' \n'.join(item.get_order() for item in self.items.all())

    get_order_list.__name__ = ' Товары в заказе'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Наименование')
    price = models.PositiveIntegerField(verbose_name='Цена единицы')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказа'

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity

    def get_order(self):
        return f"{self.product} - {self.quantity} шт. по {self.price} руб."


