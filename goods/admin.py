from django.contrib import admin
from goods.models import Category, Product, Grower


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ["name",]

@admin.register(Grower)
class GrowerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ["name",]

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable = ["discount", ]
    search_fields = ["name", "description", "grower__name"]
    list_filter = ["category", "grower__name"]
    readonly_fields = ["indica_share", "date_added"]
    fields = [
        "name",
        "category",
        "grower",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
        "flowering_time",
        "sativa_share",
        "thc",
        "date_added",
    ]

