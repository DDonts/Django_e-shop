from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # raw_id_fields = ['product']


def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', order_pdf, 'paid',
                    'first_name', 'last_name', 'email',
                    'postal_code', 'city', 'address_name',
                    'phone', 'created', 'updated',]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
