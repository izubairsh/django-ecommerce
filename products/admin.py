from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('token', 'cost', 'price', 'weight', 'meat',
                    'category', 'quantity', 'available')
    list_display_links = ('token',)
    search_fields = ('token', 'category', 'price')
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
