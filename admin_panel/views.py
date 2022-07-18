from django.template.defaultfilters import slugify
from category.forms import AddCategoryForm,AddSubCategoryForm
from category.models import Category,Sub_category
from django.shortcuts import redirect, render
from orders.models import Order, OrderProduct
from vendors.forms import AddProductForm
from store.models import Product,Images
from django.contrib import messages
from accounts.models import Account

#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.
def admin_home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            net_sales = 0
            gross_sales = 0
            shipping = 0
            tax = 0
            vendor_commission = 0
            total_orders = 0  

            sold_products = OrderProduct.objects.all()
            ordered_product = Order.objects.filter(is_ordered=True)

            for item in sold_products:
                net_sales += (item.product_price * item.quantity)
                shipping += 100


            for item in ordered_product:
                gross_sales += (item.order_total)
                tax += item.tax
                total_orders += 1
                print(total_orders)
            


            vendor_commission = net_sales * 0.90                        # 10% commission for admin

            profit = gross_sales - shipping - tax - vendor_commission
            payment = tax + shipping + vendor_commission
            context = {
                'menu':'dashboard',
                'sales':int(net_sales),
                'gross_sales':int(gross_sales),
                'payment':int(payment),
                'profit':int(profit),
                'total_orders':int(total_orders),
                }

            return render(request,'admin_panel/dashboard.html',context)
        else:
            return redirect('page_not_found')
    else:
        return redirect('login')


def page_not_found(request):
    return render(request,'admin_panel/not_found.html')


def user_accounts(request):
    if request.user.is_admin:
        context = {
            'users':Account.objects.all().filter(is_active=True),
            'menu':'Accounts',
        }
        return render(request,'admin_panel/user_accounts.html',context)
    return redirect('login')


def ban_user(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)

        email = user.email
    
        #Ban email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore Admin'
        message = render_to_string('admin_panel/user_ban_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Status email has been sent to '+email+'.')

        user.is_active = False
        user.is_staff = False
        user.is_banned = True
        user.save()
        return redirect('user_accounts')
    else:
        return redirect('login')


def unban_user(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)

        email = user.email
    
        #Ban email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore Admin'
        message = render_to_string('admin_panel/user_unban_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Status email has been sent to '+email+'.')

        user.is_active = True
        user.is_staff = False
        user.is_banned = False
        user.save()
        return redirect('user_accounts')
    else:
        return redirect('login')


def banned_accounts(request):
    if request.user.is_admin:
        context = {
            'users':Account.objects.all().filter(is_active=False,is_banned=True),
            'vendors':Account.objects.all().filter(is_staff=False,is_banned=True)
        }
        return render(request,'admin_panel/banned_accounts.html',context)
    else:
        return redirect('login')


def ban_vendor(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)

        email = user.email
    
        #Ban email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore Admin'
        message = render_to_string('admin_panel/vendor_ban_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Status email has been sent to '+email+'.')

        user.is_staff = False
        user.is_banned = True
        user.save()
        return redirect('vendor_accounts')
    else:
        return redirect('login')


def unban_vendor(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)

        email = user.email
    
        #Ban email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore Admin'
        message = render_to_string('admin_panel/vendor_unban_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Status email has been sent to '+email+'.')

        user.is_staff = True
        user.is_active = True
        user.is_banned = False
        user.save()
        return redirect('vendor_accounts')
    else:
        return redirect('login')


def vendor_accounts(request):
    if request.user.is_admin:
        context = {
            'vendors':Account.objects.all().filter(is_staff=True),
            'menu':'Accounts',
        }
        return render(request,'admin_panel/vendor_accounts.html',context)
    return redirect('login')


def vendor_requests(request):
    if request.user.is_admin:
        context = {
            'vendor_req':Account.objects.all().filter(vendor_req_status=True),
            'vendor_req_rejected':Account.objects.all().filter(vendor_req_status=False,vendor_req_rejection_status=True),
            'menu':'Accounts',
        }
        return render(request,'admin_panel/vendor_requests.html',context)
    return redirect('login')


def vendor_approve(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)

        email = user.email
    
        #Approval email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore vendor request'
        message = render_to_string('admin_panel/vendor_accept_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Approval email has been sent to '+email+'.')

        user.is_staff = True
        user.vendor_req_status = False
        user.vendor_req_rejection_status = False
        user.save()
        return redirect('vendor_requests')
    else:
        return redirect('login')


def vendor_reject(request,id):
    if request.user.is_admin:
        user = Account.objects.get(pk=id)
        email = user.email
        
        #rejection email
        current_site = get_current_site(request)
        mail_subject = 'Bitstore vendor request'
        message = render_to_string('admin_panel/vendor_rejection_email.html',{
            'user':user,
            'domain':current_site,
        })  
        to_email = email
        sent_email = EmailMessage(mail_subject,message,to=[to_email])
        sent_email.send()
        messages.success(request,'Rejection email has been sent to '+email+'.')

        user.vendor_req_status = False
        user.vendor_req_rejection_status = True
        user.save()
        return redirect('vendor_requests')
    else:
        return redirect('login')


def category_list(request):
    if request.user.is_admin:
        context = {
            'categories':Category.objects.all(),
            'menu':'categories',
        }
        return render(request,'admin_panel/categories.html',context)
    else:
        return redirect('login')
    

def sub_category_list(request):
    if request.user.is_admin:
        context = {
            'sub_categories':Sub_category.objects.all(),
            'menu':'sub_categories',
        }
        return render(request,'admin_panel/sub_categories.html',context)
    else:
        return redirect('login')


def product_list(request):
    if request.user.is_admin:
        context = {
            'products':Product.objects.all().filter(is_available=True),
            'menu':'products',
        }
        return render(request,'admin_panel/product_list.html',context)
    else:
        return redirect('login')


def unlisted_product_list(request):
    if request.user.is_admin:
        context = {
            'na_products':Product.objects.all().filter(is_available=False),
            'menu': 'products'
        }
        return render(request,'admin_panel/unlisted_product_list.html',context)
    else:
        return redirect('login')

def admin_add_product(request):
    if request.user.is_admin:
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
                return redirect('products')
        else:
            form = AddProductForm()
        context = {
            'form':form
        }
        return render(request,'admin_panel/add_product.html',context)
    else:
        return redirect('login')


def admin_edit_product(request,slug):
    if request.user.is_admin:
        product = Product.objects.get(slug=slug)
        if request.user == product.vendor:
            if request.method == "POST":
                if len(request.FILES) != 0:
                    images = Images.objects.all().filter(product=product)
                    for image in images: 
                        image.delete()

                    images = request.FILES.getlist('images')
                    print(images)
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
                        return redirect('products')
                    else:
                        return redirect('unlisted_products')
            else:
                form = AddProductForm(instance=product)

            context={
                'form':form,
                'product':product,
                'menu': 'product'

            }
            return render(request,'admin_panel/edit_product.html',context)
        else:
            messages.warning(request,'you are not allowed to edit this product')
            return redirect('products')
    else:
        return redirect('login')


def admin_product_available_status(request,id):
    if request.user.is_admin:
        product = Product.objects.get(id=id)
        if product.is_available:
            product.is_available = False
            product.unlisted_by = request.user.username
            product.save()
            messages.warning(request,'Product Status updated to Inactive.')
            return redirect('products')
        else:
            product.is_available = True
            product.unlisted_by = ''
            product.save()
            messages.info(request,'Product Status updated to Active.')
            return redirect('unlisted_products')
    else:
        return redirect('login')


def admin_add_category(request):

    if request.user.is_admin:
        if request.method == 'POST':
            form = AddCategoryForm(request.POST,request.FILES)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                description = form.cleaned_data['description']
                slug = slugify(category_name)
                cat_image = form.cleaned_data['cat_image']

                category = Category.objects.create(
                    category_name=category_name,
                    slug=slug,
                    description=description,
                    cat_image=cat_image
                    )
                return redirect('categories')
        else:
            form = AddCategoryForm()
        context={
            'form':form
        }
        return render(request,'admin_panel/add_category.html',context)
    else:
            return redirect('login')


def admin_edit_category(request,id):
    if request.user.is_admin:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            form = AddCategoryForm(request.POST,request.FILES,instance=category)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                form.save()
                category.slug=slug
                category.save()
                return redirect('categories')
        else:
            form = AddCategoryForm(instance=category)
        context={
            'form':form
        }
        return render(request,'admin_panel/add_category.html',context)
    else:
        return redirect('login')


def admin_delete_category(request,id):
    if request.user.is_admin:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('categories')
    else:
        return redirect('login')


def admin_add_sub_category(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = AddSubCategoryForm(request.POST,request.FILES)
            if form.is_valid():
                sub_category_name = form.cleaned_data['sub_category_name']
                description = form.cleaned_data['description']
                slug = slugify(sub_category_name)
                cat_image = form.cleaned_data['cat_image']

                sub_category = Sub_category.objects.create(
                    sub_category_name=sub_category_name,
                    slug=slug,
                    description=description,
                    cat_image=cat_image,
                    )
                return redirect('sub_categories')
        else:
            form = AddSubCategoryForm()
        context={
            'form':form
        }
        return render(request,'admin_panel/add_sub_category.html',context)
    else:
        return redirect('login')


def admin_edit_sub_category(request,id):
    if request.user.is_admin:
        sub_category = Sub_category.objects.get(id=id)
        if request.method == 'POST':
            form = AddSubCategoryForm(request.POST,request.FILES,instance=sub_category)
            if form.is_valid():
                sub_category_name = form.cleaned_data['sub_category_name']
                slug = slugify(sub_category_name)
                form.save()
                slug=slug
                sub_category.save()
                return redirect('sub_categories')
        else:
            form = AddSubCategoryForm(instance=sub_category)
        context={
            'form':form
        }
        return render(request,'admin_panel/add_sub_category.html',context)
    else:
        return redirect('login')


def admin_delete_sub_category(request,id):
    if request.user.is_admin:
        sub_category = Sub_category.objects.get(id=id)
        sub_category.delete()
        return redirect('sub_categories')
    else:
        return redirect('login')

