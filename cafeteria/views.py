from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.utils.timezone import datetime

from customer.models import*



class Dashboard(View):
     
    permission_required = 'admin_required'
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderItem.objects.filter(
            date_added__year=today.year, date_added__month=today.month, date_added__day=today.day)

        # loop through the orders and add the price value
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price
            
            if not order.is_shipped:
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'cafeteria/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
    
    
class OrderDetails(View):
    permission_required = 'admin_required'
    def get(self, request, pk, *args, **kwargs):
        order = OrderItem.objects.get(pk=pk)
        context = {'order': order}

        return render(request, 'cafeteria/order-details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderItem.objects.get(pk=pk)
        order.is_shipped = True
        order.save()
        
        context = {'order': order}
        return render(request, 'cafeteria/order-details.html', context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
    

# @login_required
# @permission_required('admin_required', raise_exception=True)
def addOrder(request):

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        menu = Product.objects.create( 
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=image,
        ) 
     
        return redirect('dashboard')

    context = {}
    return render(request, 'cafeteria/add.html', context)