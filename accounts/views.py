from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account, UserProfile
from orders.models import Order, OrderProduct
from . import forms
from cart.models import Cart, Cart_item
from cart.views import _cart_id

#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    UserProfile.objects.get_or_create(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'profile' : profile,
    }
    return render(request,'accounts/dashboard.html',context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            users = authenticate(request, email = email.lower(), password = password)
            if users is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = Cart_item.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = Cart_item.objects.filter(cart=cart)


                        #getting product variation by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        #getting user's product variations
                        cart_item = Cart_item.objects.filter(user=users)
                        existing_variation_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            existing_variation_list.append(list(existing_variation))
                            id.append(item.id)

                        for product_variation_item in product_variation:
                            if product_variation_item in existing_variation_list:
                                index = existing_variation_list.index(product_variation_item)
                                item_id = id[index]
                                item = Cart_item.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = users
                                item.save()
                            else:
                                cart_item = Cart_item.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = users
                                    item.save()
                except:
                    pass
                login(request,users)
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(value.split('=') for value in query.split('&'))
                    print(params)
                    if 'next' in params:
                        next_page = params['next']
                        return redirect(next_page)
                except:
                    return redirect('home')
            else:
                messages.error(request,'Enter a valid username and password')
        context={}
        return render(request,'accounts/login.html',context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = forms.UserRegistration(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                username = email.split('@')[0]
                user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                user.phone_number = phone_number

                #USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = 'please activate your account'
                message = render_to_string('accounts/acc_verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })  
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()

                user.save() #to save user after email

                # messages.success(request,'Account is successfully created for '+username+'. \nPlease check your email to activate your account.')
                return redirect('/accounts/login/?command=verification&email='+email)
        else:
            form = forms.UserRegistration()
        context = {
            'form' : form,
        } 
        return render(request,'accounts/register.html',context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        print(user)
        messages.success(request,"Congradulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__iexact=email)

            #reset password
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Email'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })  
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Password reset email has been send to your email address.')
            return redirect('login')

        else:
            messages.error(request,'Account does not exist.')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')


def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'Thid link has been expired')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull.')
            return redirect('login')
        else:
            messages.error(request,'Password does not match!, Please try again.')
            return redirect('reset_password')
    else:
        return render(request,'accounts/reset_password.html')


@login_required(login_url='login')
def my_orders(request):
    context = {
        'menu':'orders',
        'orders': Order.objects.filter(user = request.user,is_ordered = True).order_by('-created_at')
    }
    return render(request,'accounts/my_orders.html',context)


@login_required(login_url='login')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST,instance=request.user)
        profile_form = forms.UserProfileForm(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.UserProfileForm(instance=user_profile)

    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'user_profile':user_profile,
    }

    return render(request,'accounts/edit_profile.html',context)


@login_required(login_url='login')
def change_password(request):
    if request.method =="POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Password updated successfully.")
                return redirect('change_password')
       
            else:
                messages.error(request,'Current password mis-match')
                return redirect('change_password')
       
        else:
            messages.error(request,'Password does not match!')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')


@login_required(login_url='login')
def order_details(request,order_id):
    order_details = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number = order_id)
    sub_total = 0
    for item in order_details:
        sub_total += item.product_price * item.quantity

    context = {
        'order_details':order_details,
        'order':order,
        'sub_total':sub_total,
    }
    return render(request,'accounts/order_details.html',context)