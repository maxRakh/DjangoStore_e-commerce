from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename={opts.verbose_name}.csv"
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    list_editable = ['product', 'price', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_total_coast', 'first_name', 'last_name', 'phohe_number',
                    'email', 'type_of_connection', 'address', 'city',
                    'country', 'extra', 'date_ordered', 'paid', 'get_order_list', 'coupon', 'discount']
    list_filter = ['paid', 'date_ordered']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
