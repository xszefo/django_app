from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
            'orders': orders,
            'customers': customers,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'delivered': delivered,
            'pending': pending
            }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {}

    context['products'] = products
    return render(request, 'accounts/products.html', context)

def customer(request, pk=None):
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.order_set.all()
    num_of_orders = orders.count()
    context = {
            'customer': customer,
            'orders': orders,
            'num_of_orders': num_of_orders,
            }
    return render(request, 'accounts/customer.html', context)

def createOrder(request):
    context = {}
    
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context['form'] = form
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
            'form': form,
            }

    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {
            'item': order,
            }

    return render(request, 'accounts/delete.html', context)
