from django.shortcuts import render

from .models import*

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'customer/store.html', context)

def cart(request):
	context = {}
	return render(request, 'customer/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'customer/checkout.html', context)