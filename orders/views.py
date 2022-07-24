import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from cart.models import Cart_item
from proj_bitstore.settings import KEY, PAY_SECRET_KEY
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import razorpay
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# Create your views here.
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered = False, order_number=body['order_id'])

    payment = Payment.objects.create(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        payment_signature = body['razorpay_signature'],
        razor_pay_order_id = body['razorpay_order_id'],
        payment_method = body['payment_method'],
        amount_paid = body['amount_paid'],
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    #move cart_item to ordered product table
    cart_items = Cart_item.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.order_product_total = item.quantity * item.product.price
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()
        

        cart_item = Cart_item.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=order_product.id)
        orderproduct.variations.set(product_variations)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    Cart_item.objects.filter(user=request.user).delete()

    mail_subject = 'Order Placed Successfully.'
    message = render_to_string('orders/order_confirmation_email.html',{
        'user':request.user,
        'order':order,
    })  
    to_email = request.user.email
    sent_email = EmailMessage(mail_subject,message,to=[to_email])
    sent_email.send()

    data = {
        'order_number': order.order_number,
        'payment_id':payment.payment_id,
    }
    return JsonResponse(data)
        


def place_order(request,total=0,quantity=0,):
    current_user = request.user
    cart_items = Cart_item.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for item in cart_items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    tax = (2*total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.pincode = form.cleaned_data['pincode']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # to generate an order number 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date+str(data.id)
            data.order_number = order_number
            data.save()

            client = razorpay.Client(auth=(KEY, PAY_SECRET_KEY))
            DATA = {
                "amount": data.order_total * 100,
                "currency": "INR",
                "payment_capture": 1,
                # "receipt": "receipt#1",
                # "notes": { 
                #     "key1": "value3",
                #     "key2": "value2"
                # }
            }
        payment = client.order.create(data=DATA)
        
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'payment':payment
        }
        return render(request,'orders/payments.html',context)
            
    return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get("order_number")
    payment_id = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)
        sub_total = 0
        for item in ordered_products:
            sub_total += item.product_price * item.quantity

        context = {
            'order':order,
            'ordered_products':ordered_products,
            'sub_total':sub_total,
        }
        return render(request,'orders/order_complete.html',context)

    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
