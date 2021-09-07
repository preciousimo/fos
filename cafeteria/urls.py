from django.urls import path
from .views import Dashboard, OrderDetails
from . import views

urlpatterns = [
	path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('add/', views.addOrder, name='add'), 
]