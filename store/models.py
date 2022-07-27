from django.urls import reverse
from accounts.models import Account
from category.models import Category,Sub_category
from django.db import models

# Create your models here.



class Product(models.Model):
    vendor = models.ForeignKey(Account,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200,unique=True)
    author = models.CharField(max_length=250,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(blank=True)
    primary_image = models.ImageField(upload_to='photos/products/vendors/mandatory')
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category,on_delete=models.CASCADE,default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    unlisted_by = models.CharField(max_length=100,blank=True,null=True)
    is_top = models.BooleanField(default=False)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.sub_category.slug,self.slug])

    def __str__(self):
        return self.product_name



class Images(models.Model):
    image = models.ImageField(upload_to='photos/products/vendors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name


class VariationManager(models.Manager):
    def book_type(self):
        return super(VariationManager,self).filter(variation_category = 'book_type',is_active = True)

    def language(self):
        return super(VariationManager,self).filter(variation_category = 'language',is_active = True)


variation_category_choice = (
    ('book_type','book_type'),
    ('language','language')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class VariationSample(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/carousel')
    is_visible = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_top = models.BooleanField(default=True)

    def __str__(self):
        return self.title