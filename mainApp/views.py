from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,  get_object_or_404
from mainApp.models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View
# Create your views here.
def index(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {
        'categories': categories, 
        'menu_items': menu_items
         }   
    return render (request, 'index.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(MenuItem, pk=product_id)
    session_key = request.session.session_key
    cart, created = CartItem.objects.get_or_create(session_key=session_key, product=product)

    if not created:
        cart.quantity += 1
        cart.save()

    # Return a JSON response with the message and status
    response_data = {'message': 'Item added to the cart successfully', 'status': 'success'}
    return JsonResponse(response_data)

def get_cart_count(request):
    session_key = request.session.session_key
    cart_count = CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': cart_count})

def cart_detail(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    # Calculate total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    # Calculate the final total of all products
    total_price = sum(item.total_price for item in cart_items)
    request.session['cart_items_count'] = cart_items_count
    categories = Category.objects.all()
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories,
    }
    return render(request, 'cart.html', context)



def checkout(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    categories = Category.objects.all()
    # Calculate total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    # Calculate the final total of all products
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories,
    }

    return render(request, 'checkout.html', context)

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        CartItem.objects.filter(id=item_id).delete()
    return redirect('cart_detail')
def send_sms_notification(order_type):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_body = f'Hello, a new {order_type} order has been created. Check the admin panel for details.'
    message = client.messages.create(
        body=message_body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to='' 
    )
def place_order(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    total_price = sum(item.total_price for item in cart_items)
    # Create the order
    order = Order.objects.create(
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        country=request.POST.get('country'),
        total_price=total_price
    )
    order.save() 
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            image=cart_item.product.image,
            price=cart_item.product.price
        )

    cart_items.delete()

    html_content = render_to_string('order_email_template.html', {'order': order})
    text_content = strip_tags(html_content)  # Remove HTML tags for plain text email

    # Send email
    subject = 'New Order Created'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['']

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
    # send_sms_notification('Order')
    messages.success(request, 'Your Order has been received, We shall contact you soon')
    return redirect('index')

def buy_now(request):
    order2 = BuyNow2.objects.create(
        name = request.POST.get('name'),
        phone_number = request.POST.get('phone_number'),
        product_name = request.POST.get('product_name'),
        product_price = request.POST.get('product_price'),
        product_id = request.POST.get('product_id'),
        product_brand = request.POST.get('product_brand'),
        product_category = request.POST.get('product_category'),
    )
    order2.save()
    html_content = render_to_string('buy_now_email_template.html', {'order2': order2})
    text_content = strip_tags(html_content) 

    # Send email
    subject = 'New Order Created (Buy Now)'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['']

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
    send_sms_notification('Buy Now Order')
    messages.success(request, 'Your Order has been received, We shall contact you soon')
    return redirect('index')
