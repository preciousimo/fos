from django.shortcuts import render

def store(request):
	context = {}
	return render(request, 'customer/store.html', context)

def cart(request):
	context = {}
	return render(request, 'customer/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'customer/checkout.html', context)