from urllib import request
from django.shortcuts import render
from django.urls import is_valid_path #permite renderizar el codigo html que se genere en el backend
from store.models import Product

def home(request):
    #obtener productos de la DB
    products = Product.objects.all().filter(is_available=True)

    #envuelvo el resultado de producto en un diccionario (el context)
    context = {
        'products': products,
    }
    #return render(request, 'home.html')
    return render(request, 'home.html', context)#le agrego el contenido que quiero pasar a la vista
