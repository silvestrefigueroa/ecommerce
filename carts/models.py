from django.db import models

from store.models import Product


# Create your models here.
#CARRO
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

#ITEM del CARRO.
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):#esto es para que en el modulo admin me imprima lo que retorno
        return self.product.product_name

    def sub_total(self):#la llama desde el template despues
        return (self.product.price * self.quantity)

    def __unicode__(self):
        return self.product
