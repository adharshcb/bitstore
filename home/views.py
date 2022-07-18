from django.shortcuts import render
from store.models import Product,Carousel

def home(request):
    products = Product.objects.all().filter(is_available=True,is_top=True)
    carousel = Carousel.objects.all().filter(is_visible=True)
    featured = Carousel.objects.all().filter(is_visible=True,is_featured=True)
    all_products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
        'banners':carousel,
        'featured':featured,
        'all':all_products
    }
    return render(request,'home/index.html',context)
