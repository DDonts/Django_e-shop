from django.contrib import admin

from .models import Product, Category, SpecificationsItem


admin.site.index_template = 'memcache_status/admin_index.html'


class SpecsInLine(admin.TabularInline):
    model = SpecificationsItem


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    fields = ['title', 'category', 'slug', 'description', 'price', 'image', 'available']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [SpecsInLine]
    list_filter = ['category']
    list_display = ['title', 'category', 'price', 'available', 'created', 'updated']
    list_editable = ['price', 'available']


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}



