from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context ['form'] = form
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

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

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
            'customer': customer,
            'orders': orders,
            'num_of_orders': num_of_orders,
            'myFilter': myFilter,
            }
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    context = {}
    
    customer = Customer.objects.get(id=pk)
    
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context['formset'] = formset
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

    return render(request, 'accounts/update_order.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {
            'item': order,
            }

    return render(request, 'accounts/delete.html', context)
