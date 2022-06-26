from django.contrib import admin

from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    #lo que quiero listar en el grid
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)#con esta linea alcanza para que lo registre y tome por default. lo del ProductAdmin es una redefinicion no requerida
