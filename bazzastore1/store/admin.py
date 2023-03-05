from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'get_html_photo', 'slug', 'color', 'size', 'price', 'amount', 'time_create', 'time_update')
    list_filter = ('is_published', 'time_create')
    list_editable = ('is_published', 'amount', 'price')
    prepopulated_fields = {'slug': ('title',)}

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='60' />".format(obj.photo.url))

    get_html_photo.__name__ = 'Фото'

