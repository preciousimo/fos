from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm
from . import forms
from django.contrib.auth.models import User

from .models import*
from .utils import cookieCart, cartData, guestOrder


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request, template_name="registration/register.html", context={"register_form":form})

def index(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems':cartItems}
    return render(request, 'customer/index.html', context)


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems':cartItems}
     
    return render(request, 'customer/about.html', context)


def menu(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'customer/menu.html', context)

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'customer/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'customer/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body )
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            
    else:
        customer, order = guestOrder(request, data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            location = data['shipping']['location'],
        )
            
    return JsonResponse('Payment complete!', safe=False)

def confirmation(request, pk):
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    if request.method == 'GET':
        order =  OrderItem.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.product.name,
            'price': order.product.price,
            'cartItems':cartItems,
        }

        return render(request, 'customer/confirmation.html', context)