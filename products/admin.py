from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.

admin.site.register(Category)
admin.site.register(Review)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created', 'updated')
    list_filter = ('category', )