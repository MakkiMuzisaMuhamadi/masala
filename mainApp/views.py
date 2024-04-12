from django import forms
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
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
    menu_items = MenuItem.objects.all()[:12]
    grocery_items = Grocery.objects.all()[:12]
    banner = Banner.objects.first()
    banner1 = Food_Banner_1.objects.first()
    banner2 = Food_Banner_2.objects.first()
    questions = FAQ.objects.all()
    context = {
        'categories': categories, 
        'menu_items': menu_items,
        'banner': banner,
        'banner1': banner1,
        'banner2': banner2,
        'grocery_items': grocery_items,
        'questions': questions,
         }   
    return render (request, 'index.html', context)


def add_to_cart(request, product_type, product_id):
    if product_type == 'MenuItem':
        product = get_object_or_404(MenuItem, pk=product_id)
    elif product_type == 'Grocery':
        product = get_object_or_404(Grocery, pk=product_id)
    else:
        return JsonResponse({'error': 'Invalid product type'}, status=400)

    # Create or update CartItem
    cart_item, created = CartItem.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(product.__class__),
        object_id=product.id,
        session_key=request.session.session_key
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

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

def orderme(request, model_name, item_id):
    if model_name == 'product':
        item = Food_Banner_1.objects.get(id=item_id)
    elif model_name == 'anothermodel':
        item = Banner.objects.get(id=item_id)
    elif model_name == 'yetanothermodel':
        item = Food_Banner_2.objects.get(id=item_id)
    elif model_name == 'MenuItem':
        item = MenuItem.objects.get(id=item_id)
    elif model_name == 'Grocery':
        item = Grocery.objects.get(id=item_id)
    else:
        return HttpResponseBadRequest("Invalid model name or ID")

    context = {'item': item}
    return render(request, 'orderme.html', context)

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
        content_type = ContentType.objects.get_for_model(cart_item.product.__class__)

        # Create the OrderItem using the GenericForeignKey fields
        OrderItem.objects.create(
            order=order,
            content_type=content_type,
            object_id=cart_item.product.id,
            quantity=cart_item.quantity,
            image=cart_item.product.image_main,
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
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('first_name')
        phone_number = request.POST.get('phone')
        product_name = request.POST.get('product_name')
        address = request.POST.get('address')
        product_price = request.POST.get('product_price')
        product_id = request.POST.get('item_id')

 
        order2 = BuyNow2.objects.create(
            name=name,
            phone_number=phone_number,
            product_name=product_name,
            product_price=product_price,
            product_id=product_id,
            address=address,
        )
        order2.save()
        messages.success(request, 'Your order has been received. We will contact you soon.')
        return redirect('index')

    return redirect('index')

def grocery_items_view(request):

    grocery_items = Grocery.objects.all()

    return render(request, 'grocery.html', {'grocery_items': grocery_items,})

def menu_items_view(request):

    menu_items = MenuItem.objects.all()

    return render(request, 'foods.html', {'menu_items': menu_items,})

def search_items(request):
    query = request.GET.get('q')
    menu_items = MenuItem.objects.filter(name__icontains=query) if query else MenuItem.objects.none()
    grocery_items = Grocery.objects.filter(name__icontains=query) if query else Grocery.objects.none()
    
    items_found = bool(menu_items.exists() or grocery_items.exists())  # Flag indicating if any items were found

    return render(request, 'search.html', {'menu_items': menu_items, 'grocery_items': grocery_items,'items_found': items_found, 'query': query})