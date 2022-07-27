from django.shortcuts import redirect, render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import requests


# Create your views here.
def wishlist(request,wishlist_items=None):
    if request.user.is_authenticated:
        try:
            wishlist_items = Wishlist.objects.all().filter(user=request.user).order_by('product')
            product = Product.objects.all()

        except ObjectDoesNotExist:  
            pass
        context = {
            'cart_items':wishlist_items,
            'all':product,
        }
        return render(request,'store/wishlist.html',context)
    else:
        return redirect('login')


# def add_wishlist(request,product_id):
#     product = Product.objects.get(id=product_id)
#     current_user = request.user
#     product_variation = []
#     if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
#                 try:
#                     variation = Variation.objects.get(
#                         product = product,
#                         variation_category__iexact=key,
#                         variation_value__iexact = value,
#                         )
#                     product_variation.append(variation)
#                 except:
#                     pass
                
#     is_cart_item_exists = Wishlist.objects.filter(product=product,user=current_user).exists()
#     if is_cart_item_exists: 
#         cart_item = Wishlist.objects.filter(product=product,user=current_user)

#         existing_variation_list = []
#         id = []
#         for item in cart_item:
#             existing_variation = item.variations.all()
#             existing_variation_list.append(list(existing_variation))
#             id.append(item.id)

#             if product_variation in existing_variation_list:
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = Wishlist.objects.get(product=product,id=item_id)
#                 # item.quantity += 1
#                 item.save()

#             else:
#                 item = Wishlist.objects.create(
#                         product=product,
#                         # quantity=1,
#                         user=current_user
#                         )   
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()

#     else:
#         cart_item = Wishlist.objects.create(
#             product = product,
#             # quantity = 1,
#             user=current_user
#         )
#         if len(product_variation) > 0:
#             cart_item.variations.clear()
#             cart_item.variations.add(*product_variation)
#         cart_item.save()

#     return redirect ('wishlist')


def add_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    is_wishlist_exist = Wishlist.objects.filter(user=request.user,product=product).exists()
    if is_wishlist_exist:
        pass
    else:
        wishlist = Wishlist.objects.create(
            user = request.user,
            product = product
        )
    return redirect('wishlist')
    # url = request.META.get('HTTP_REFERER')
    # try:
    #     query = requests.utils.urlparse(url).query
    #     params = dict(value.split('=') for value in query.split('&'))
    #     if 'next' in params:
    #         next_page = params['next']
    #         return redirect(next_page)
    # except:
    #     return redirect('wishlist')


def remove_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item = Wishlist.objects.get(user=request.user,product=product_id)
    wishlist_item.delete()
    return redirect('wishlist')