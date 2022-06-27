from ctypes import create_unicode_buffer
from .models import Cart,CartItem
from .views import _cart_id

def counter(request):#repasar este punto
    cart_count = 0
    try:
        #busco el carro
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        #busco los elementos de ese carro
        cart_items = CartItem.objects.all().filter(cart=cart[:1])#repasar no entendi por que la coleccion y solo 1
        #debe leer cada linea y obtener el quantity de cada uno y sumarlas entre si:
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
