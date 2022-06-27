from itertools import product
from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Product
from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(is_available=True, category=categories)
        products_count = products.count()
    
    else:
        #obtengo los productos habilitados
        products = Product.objects.all().filter(is_available=True)
        #para la cuenta de productos
        products_count = products.count()
    #los empaqueto en el contexto que mando al template como contenido dinamico

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    #valido por si lo que me pasas el usuario no existe:
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)#el doble guion bajo es para traer el VALOR del campo slug en la clase category
        
        #ver si este producto ya esta agregado al carrito: (es bool)
        in_cart = (CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product)).exists()
    
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)