from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "label")
    search_fields = ("title", "label")
    list_filter = ("price",)
