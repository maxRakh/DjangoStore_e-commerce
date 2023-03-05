from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    valid_from = models.DateTimeField(verbose_name='Действителен от')
    valid_before = models.DateTimeField(verbose_name='Действителен до')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Размер скидки %')
    active = models.BooleanField(verbose_name='Действует')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

