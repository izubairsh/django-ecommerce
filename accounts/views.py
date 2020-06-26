from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order_items.models import OrderItem
from packages.models import Package
from orders.models import Order
from customers.models import Customer
from products.models import Product
from datetime import datetime


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
        else:
            return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    today = datetime.today()
    orders = Order.objects.all()
    customers = Customer.objects.all().count()
    products = Product.objects.all().filter(available=True).count()
    new_order = 0
    total = 0
    cost = 0
    for o in orders:
        if today.month == o.date_created.month:
            total += o.get_cart_total
            cost += o.get_cost
        if not o.get_status:
            new_order += 1
    items = OrderItem.objects.all().filter(product=None)
    packages = Package.objects.all()
    arr = []
    for p in packages:
        temp = items.filter(package=p)
        c = {
            'package': p,
            'count': temp.count()
        }
        arr.append(c)
    print(arr)
    context = {
        'new_orders': new_order,
        'customers': customers,
        'orders': orders.count(),
        'products': products,
        'revenue': total,
        'cost': cost,
        'profit': total-cost,
        'expense': 500,
        'arr': arr,
        'year': today.year,
        'month': today.strftime("%B")
    }
    return render(request, 'dashboard.html', context)
