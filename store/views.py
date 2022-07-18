from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, Cart_item
from category.models import Category
from .models import Product,Images
from cart.views import _cart_id
from django.db.models import Q

#paginator
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    all_products = Product.objects.all().filter(is_available=True)
    context = { 
        'products': paged_products,
        'product_count':product_count,
        'all':all_products
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = Cart_item.objects.filter(cart__cart_id = _cart_id(request),product = single_product).exists()
        images = Images.objects.filter(product=single_product)
    except Exception as e:
        raise e

    all_products = Product.objects.all().filter(is_available=True)
    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'images':images,
        'all':all_products
    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains = keyword) |
                Q(product_name__icontains = keyword) |
                Q(author__icontains = keyword)
            )
            paginator = Paginator(products,6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()

            context = {
                'products': paged_products,
                'product_count':product_count,
            }
            return render(request,'store/store.html',context)
        else:
            return redirect('store')
    else:
        return redirect('store')
    