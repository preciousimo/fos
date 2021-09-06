from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.index, name="index"),
 	path('menu', views.menu, name="menu"),
  	path('about', views.about, name="about"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
 	path('update_item/', views.updateItem, name="update_item"),
  	path('process_order/', views.processOrder, name="process_order"),
   
   path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
]