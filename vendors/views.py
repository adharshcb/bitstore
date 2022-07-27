from django.template.defaultfilters import slugify
from category.models import Category,Sub_category
from django.shortcuts import redirect, render
from orders.models import Order, OrderProduct
from vendors.forms import AddProductForm
from store.models import Product,Images
from django.contrib import messages
from accounts.models import Account, UserProfile

from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth,TruncMinute,TruncDay
import datetime
from django.db.models import Q

#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from wishlist.models import Wishlist


# Create your views here.

def vendor_reg(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.vendor_req_status:
                messages.error(request,"You have already submitted the appication !. Please wait till admin's approval.")
            elif request.user.is_staff:
                return redirect('vendor_dashboard')
            else:
                request.user.vendor_store = request.POST['store_name']
                request.user.vendor_req_status = True

                user = request.user
                admin = Account.objects.get(is_mail_manager=True)
                email = admin.email
                #USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = 'please activate your account'
                message = render_to_string('accounts/vendor_account_activation_email.html',{
                    'user':user,
                    'admin':admin,
                    'domain':current_site,
                })  
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                
                request.user.save()
                messages.error(request,"You have successfully submitted the appication !. Please wait till admin's approval.")

                
        context = {
        } 
        return render(request,'vendors/vendor_registration.html',context)
    else:
        return redirect('login')

def vendor_dashboard(request):
    if request.user.is_staff:

        try:
            sold_products = OrderProduct.objects.all().filter(product__vendor=request.user).order_by('-created_at')
        except:
            pass

        try:
            net_sales = OrderProduct.objects.filter(product__vendor=request.user).aggregate(sum = Sum('order_product_total'))['sum']
        except:
            pass

        if net_sales == None:
            net_sales = 0


        tax = net_sales * 0.02                                          # 2% tax on total

        gross_sales = net_sales + tax

        total_orders = OrderProduct.objects.all().filter(product__vendor=request.user).count()

        vendor_commission = net_sales * 0.90                            # 10% commission for admin
        profit = net_sales * 0.10

        payment = tax + profit

        products_in_wishlist = Wishlist.objects.filter(product__vendor = request.user).count()

        variation_count = OrderProduct.objects.all().filter(product__vendor=request.user).aggregate(
            # ebook = Count('variations',filter=Q( v = variations['ebook']))
        )

        chart_year = datetime.date.today().year
        chart_month = datetime.date.today().month

        daily_revenue = OrderProduct.objects.filter(created_at__year=chart_year,created_at__month=chart_month,product__vendor=request.user).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_product_total')).values('day','sum')

        day=[]
        revenue=[]
        for i in daily_revenue:
            day.append(i['day'].minute)
            revenue.append(int(i['sum']))

        context = {
            'menu':'dashboard',
            'sales':int(net_sales),
            'gross_sales':int(gross_sales),
            'payment':int(payment),
            'profit':int(profit),
            'total_orders':int(total_orders),
            'vendor_commission':int(vendor_commission),
            'sold_products':sold_products,
            'products_in_wishlist':products_in_wishlist,
            'day':day,
            'revenue':revenue,
            }

        return render(request,'vendors/dashboard.html',context)
    else:
        return redirect('vendor_registration')


def order_Pending_list(request):
    if request.user.is_staff:
        context = {
            'order_list':OrderProduct.objects.filter(product__vendor=request.user,order__status='New')
        }
        return render(request,'vendors/order_Pending_list.html',context)


def cancelled_orders(request):
    if request.user.is_staff:
        context = {
            'order_list':OrderProduct.objects.filter(product__vendor=request.user,order__status='Cancelled')
        }
        return render(request,'vendors/order_cancelled_list.html',context)


def completed_orders(request):
    if request.user.is_staff:
        context = {
            'order_list':OrderProduct.objects.filter(product__vendor=request.user,order__status='Completed')
        }
        return render(request,'vendors/order_completion_list.html',context)


def category_list(request):
    if request.user.is_staff:
        context = {
            'categories':Category.objects.all(),
            'menu': 'categories'
            
        }
        return render(request,'vendors/categories.html',context)
    return redirect('vendor_registration')

def sub_category_list(request):
    if request.user.is_staff:
        context = {
            'subcategories':Sub_category.objects.all(),
            'menu': 'categories'
        }
        return render(request,'vendors/sub_categories.html',context)
    return redirect('vendor_registration')


def product_list(request,id):
    if request.user.is_staff:
        context = {
            'products':Product.objects.all().filter(vendor=id,is_available=True),
            'menu': 'product'
        }
        return render(request,'vendors/product_list.html',context)


def unlisted_product_list(request,id):
    if request.user.is_staff:
        context = {
            'na_products':Product.objects.all().filter(vendor=id,is_available=False),
            'menu': 'product'
        }
        return render(request,'vendors/unlisted_product_list.html',context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            stock = form.cleaned_data['stock']
            is_available = form.cleaned_data['is_available']
            author = form.cleaned_data['author']
            vendor = request.user
            slug = slugify(product_name)
            primary_image = form.cleaned_data['primary_image']

            product = Product.objects.create(
                vendor = vendor,
                product_name=product_name,
                slug=slug,
                category=category,
                description=description,
                price=price,
                stock=stock,
                is_available=is_available,
                author=author,
                sub_category=sub_category,
                primary_image=primary_image
                )
            
            images = request.FILES.getlist('images')
            for image in images:
                Images.objects.create(
                    image=image,
                    product=product
                )
            return redirect('vendor_products',id=request.user.id)
    else:
        form = AddProductForm()
    context = {
        'form':form,
        'menu': 'product'
    }
    return render(request,'vendors/add_product.html',context)

def edit_product(request,slug):
    product = Product.objects.get(slug=slug)

    if request.method == "POST":
        if len(request.FILES) != 0:
            images = Images.objects.all().filter(product=product)
            for image in images: 
                image.delete()

            images = request.FILES.getlist('images')
            for image in images:
                Images.objects.create(  
                    image=image,
                    product=product
                )

        form = AddProductForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            messages.success(request,'Product updates successfully.')
            if product.is_available:
                return redirect('vendor_products',id=request.user.id)
            else:
                return redirect('vendor_unlisted_product',id=request.user.id)

    form = AddProductForm(instance=product)

    context={
        'form':form,
        'product':product,
        'menu': 'product'

    }
    return render(request,'vendors/edit_product.html',context)



def product_available_status(request,id):
    product = Product.objects.get(id=id)
    if product.is_available:
        product.is_available = False
        product.unlisted_by = request.user.username
        product.save()
        messages.warning(request,'Product Status updated to Inactive.')
        return redirect('vendor_products',id=request.user.id)
    else:
        product.is_available = True
        product.unlisted_by = ''
        product.save()
        messages.info(request,'Product Status updated to Active.')
        return redirect('vendor_unlisted_product',id=request.user.id)
