from django.contrib import admin
from goods.models import Category, Product, Grower


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

@admin.register(Grower)
class GrowerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    