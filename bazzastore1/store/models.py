from django.db import models
from django.urls import reverse


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название товара', null=True)
    color = models.CharField(max_length=255, verbose_name='Цвет товара', null=True)
    size = models.CharField(max_length=255, verbose_name='Размер товара', null=True)
    price = models.IntegerField(verbose_name='Цена товара')
    amount = models.IntegerField(default=0, verbose_name='Остаток товара')
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание товара', null=True)
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото товара', null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания карточки товара')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения карточки товара')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class Category(models.Model):
    ordering = ('id',)
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])
