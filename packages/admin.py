from django.contrib import admin
from .models import Package


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_weight', 'max_weight', 'min_meat', 'max_meat', 'category', 'price')
    list_display_links = ('name',)
    search_fields = ('name', 'type', 'price')
    list_per_page = 25


admin.site.register(Package, PackageAdmin)
