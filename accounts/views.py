from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order_items.models import OrderItem
from packages.models import Package
from orders.models import Order
from customers.models import Customer
from products.models import Product
from expenses.models import Expense
from datetime import datetime
from django.core.paginator import Paginator


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

    expenses = Expense.objects.all().filter(year=today.year)
    paginator = Paginator(expenses, 1)
    page = request.GET.get('page')
    paged_expenses = paginator.get_page(page)
    expense = sum([e.amount for e in expenses])

    orders = Order.objects.all()
    customers_count = Customer.objects.all().count()
    products_count = Product.objects.all().filter(available=True).count()
    products = Product.objects.all()

    cost = cost1 = total = new_order = 0
    for o in orders:
        if o.date_created:
            if today.month == o.date_created.month:
                cost1 += o.get_cost
                total += o.get_total_paid
        if not o.get_status:
            new_order += 1

    for product in products:
        if product.date_created
        if today.month == product.date_created.month:
            cost += product.cost
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
    context = {
        'new_orders': new_order,
        'customers': customers_count,
        'orders': orders.count(),
        'products': products_count,
        'revenue': total,
        'cost': cost,
        'profit': total-cost1,
        'arr': arr,
        'year': today.year,
        'month': today.strftime("%B"),
        'expenses': paged_expenses,
        'expense': expense
    }
    return render(request, 'dashboard.html', context)
