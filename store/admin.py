from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price', 'original_price', 'stock', 'available', 'is_featured', 'is_bestseller']
    list_filter   = ['available', 'category', 'is_featured', 'is_bestseller']
    list_editable = ['price', 'stock', 'available', 'is_featured', 'is_bestseller']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created']