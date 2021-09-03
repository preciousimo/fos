from django.shortcuts import render

from .models import*

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'customer/store.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {'items':items}
    return render(request, 'customer/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'customer/checkout.html', context)