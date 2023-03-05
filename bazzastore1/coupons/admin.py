from django.contrib import admin
from .models import *


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_before', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_before']
    search_fields = ['code']