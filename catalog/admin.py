from django.contrib import admin
from catalog.models import Product, Category, ContactInfo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'category', 'is_published', 'owner')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')
    search_fields = ('id', 'name', 'email', 'phone',)
