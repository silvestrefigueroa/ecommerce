from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product
from carts.models import Cart, CartItem

# Create your views here.

def _cart_id(request):#como es una funcion privada, le pone el _alPrincipio
    #basicamente, devuelve el id de la sesion, si no existe la crea. Ese id se usa para nombrar al Cart luego
    cart = request.session.session_key
    if not cart:#crearlo si no existe la sesion, creao ahora
        cart = request.session.create()#crea una sesion si no existia
    #sea que existiera o se cree, se retorna el cart (id de la sesion)
    return cart

def add_cart(request, product_id):#la funcion requiere recibir el id del producto a agregar al carro
    #obtengo el objeto Producto a partir del id que recibo por parametro
    product = Product.objects.get(id=product_id)
    #como no se si existe el carro, uso try (la idea es que si no existe, lo creo)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#buscar al carrito en la sesion - Notar como la llama a la funcion privada de una sin el self
    except Cart.DoesNotExist:#no chilla, si no existe lo manda a crear.
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()#para disprar el evento y se haga el nuevo registro en la DB
    #agregar al carro el cartItem y vincularlo con el producto
    try:#suponiendo que estoy encontrando el CartItem
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity +=1#cada vez que sea el mismo producto, se aumentara en 1
        cart_item.save()
    except CartItem.DoesNotExist:#y si no existia previamente este CartItem
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    #obtengo el carro, a partir de request y cart id
    cart = Cart.objects.get(cart_id=_cart_id(request))
    #obtengo el objeto del producto con el product_id recibido por parametro
    product = get_object_or_404(Product, id=product_id)
    #con el objeto producto, filtro el cart_item que tiene ese producto y ese carro
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    #redirigir al carro
    return redirect('cart')#cuando usar redirect y cuando un render??

def remove_cart_item(request, product_id):
    #obtengo los 2 elementos para identificar el cart_item: el producto y el carro
    #carro
    cart = Cart.objects.get(cart_id=_cart_id(request))
    #producto (obj)
    product = get_object_or_404(Product, id=product_id)#estudiar cuando usar este 404 y que otras formas hay de hacerlo 
    #con los dos elementos, determinar el cart_item:
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')#cuando usar redirect y cuando un render??


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        #hago este bucle para saber el total en plata y cantidad de productos
        for cart_item in cart_items:
            quantity += cart_item.quantity
            total += (cart_item.product.price * cart_item.quantity)

        #normalmente el TAX es un % de la compra (debiera ser configurable no hardocdeado aca)
        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        print("Entro a la excepcion")
        pass ##ignorar la excepcion
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request,'store/cart.html', context)

