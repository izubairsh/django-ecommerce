from django.contrib import admin
from .models import *


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity',
                    'package', 'day', 'time', 'get_total', 'complete', 'processing', 'ready', 'delivered')
    list_display_links = ('id', 'order')
    search_fields = ('id', 'order')
    list_per_page = 25


admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Time)
