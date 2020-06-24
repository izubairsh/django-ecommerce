from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'get_cart_total', 'get_total_paid', 'get_balance', 'get_payable',
                    'complete', 'refund', 'date_created')
    list_display_links = ('id', 'customer')
    search_fields = ('id', 'customer', 'date_created')
    list_per_page = 25


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction)
