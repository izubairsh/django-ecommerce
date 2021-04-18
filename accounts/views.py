from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order_items.models import OrderItem
from packages.models import Package
from orders.models import Order
from customers.models import Customer
from products.models import Product, Category
from expenses.models import Expense
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q


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
    sellectedYear = today.year
    if 'sellectedYear' in request.GET:
        sellectedYear = request.GET['sellectedYear']
    expenses = Expense.objects.all().filter(year=sellectedYear)
    paginator = Paginator(expenses, 1)
    page = request.GET.get('page')
    paged_expenses = paginator.get_page(page)
    expense = sum([e.amount for e in expenses])

    orders = Order.objects.all().filter(complete=True)
    customers_count = Customer.objects.all().count()
    items = OrderItem.objects.all()
    packages = Package.objects.all()
    products = Product.objects.all()
    products = products.filter(
        Q(date_created__icontains=sellectedYear)
    ).distinct()
    orders = orders.filter(
        Q(date_created__icontains=sellectedYear)
    ).distinct()
    items = items.filter(
        Q(date_added__icontains=sellectedYear)
    ).distinct()
    total_cost = sum([order.get_cost for order in orders])
    total_revenue = sum([order.get_sub_total for order in orders])
    total_balance = sum([order.get_balance for order in orders])
    product_cost = sum([product.cost for product in products])

    total_booking = []
    for package in packages:
        c = {
            'package': package,
            'count': items.filter(package=package).count()
        }
        total_booking.append(c)

    categories = Category.objects.all()
    total_stock = []
    for cat in categories:
        temp = products.filter(category=cat)
        c = {
            'category': cat,
            'count': temp.count()
        }
        total_stock.append(c)
    context = {
        'new_orders': orders.count(),
        'customers': customers_count,
        'orders': orders.count(),
        'products': products.count(),
        'revenue': total_revenue,
        'balance': total_balance,
        'product_cost': product_cost,
        'profit': total_revenue-total_cost,
        'total_booking': total_booking,
        'total_stock': total_stock,
        'expenses': paged_expenses,
        'expense': expense,
        'sellectedYear': sellectedYear
    }
    return render(request, 'dashboard.html', context)
