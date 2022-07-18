from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name