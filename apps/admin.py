from django.contrib import admin

from apps.models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass





@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass
