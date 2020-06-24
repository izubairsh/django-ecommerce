from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.utils import cart_data
import json
from datetime import datetime

from .models import Order, Transaction
from order_items.models import OrderItem, Time
from customers.models import Customer
from products.models import Product, Category
from packages.models import Package
from customers.forms import CustomerForm

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.core import serializers


@login_required(login_url='login')
def orders(request):
    q = d = r = ''

    orders = Order.objects.order_by('-date_created').filter(complete=True)
    if 'q' in request.GET:
        q = request.GET['q']
        orders = orders.filter(
            Q(id__icontains=q) |
            Q(customer__name__icontains=q) |
            Q(customer__phone__icontains=q)
        ).distinct()
    if 'r' in request.GET:
        r = request.GET['r']
        if not r == "":
            orders = orders.filter(refund=r)
    if 'd' in request.GET:
        d = request.GET['d']
        if not d == "":
            if 'True' in d:
                a = True
            else:
                a = False
            orders = [x for x in orders if x.get_status == a]
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        'orders': paged_orders,
        'query': q,
        'r': r,
        'd': d
    }
    return render(request, 'orders/index.html', context)


@login_required(login_url='login')
def order(request, pk):
    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()
    transactions = order.transaction_set.all()
    context = {
        'order': order,
        'items': items,
        'transactions': transactions
    }
    return render(request, 'orders/order.html', context)


@login_required(login_url='login')
def order_form(request, pk=0):
    user = request.user
    # Get Order
    if pk == 0:
        order, created = Order.objects.get_or_create(user=user, complete=False)
    else:
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            order = None

    order.date_created = datetime.now()
    order.save()
    q = ''
    categories = Category.objects.all()
    t = categories.first()

    if 'type' in request.GET:
        t = Category.objects.get(name=request.GET['type'])
    products = Product.objects.order_by(
        '-date_created').filter(category=t, available=True)

    if 'q' in request.GET:
        q = request.GET['q']
        products = products.filter(
            Q(token__icontains=q) |
            Q(price__icontains=q)
        ).distinct()

    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    packages = Package.objects.order_by('-date_created')
    times = Time.objects.all()
    items = order.orderitem_set.order_by('-date_added')
    try:
        transactions = Transaction.objects.filter(order=order)
    except Transaction.DoesNotExist:
        transactions = None

    context = {
        'packages': packages,
        'products': paged_products,
        'query': q,
        'type': t.name,
        'items': items,
        'order': order,
        'categories': categories,
        'times': times,
        'transactions': transactions
    }
    return render(request, 'orders/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    if request.POST:
        customer = None
        phone = request.POST['phone']
        try:
            customer = Customer.objects.get(phone=phone)
            customer.deleted = False
            customer.save()
            form = CustomerForm(request.POST, instance=customer)
        except Customer.DoesNotExist:
            print('not exist')
        if customer == None:
            form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            user = request.user
            order, created = Order.objects.get_or_create(
                user=user, complete=False)
            order.customer = customer
            order.save()
            return redirect('invoice')
    else:
        form = CustomerForm()
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cart_items': cart_items, 'form': form}
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def invoice(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'orders/invoice.html', context)


@login_required(login_url='login')
def complete_order(request):
    data = cart_data(request)
    order = data['order']
    order.complete = True
    order.save()
    return redirect('orders')


@login_required(login_url='login')
def get_customer(request):
    data = json.loads(request.body)
    phone = data['phone']
    try:
        customer = Customer.objects.get(phone=phone)
        response = {
            "name": customer.name,
            "phone": customer.phone,
            "address": customer.address,
        }
    except Customer.DoesNotExist:
        customer = None
        response = None

    return JsonResponse(response, safe=False)


def cart(request):
    if request.POST:
        update = request.POST["update"]
        advance = request.POST["advance"]
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=False)
        order.advance = advance
        order.save()

        if '1' in update:
            return redirect('orders')
        return redirect('checkout')


def refund_order(request, pk):
    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()

    for i in items:
        if not i.delivered:
            product = Product.objects.get(id=i.product.id)
            print(product)
            product.quantity += i.quantity
            product.available = True
            product.save()

    order.refund = True
    order.save()

    return redirect('orders')


def add_trans(request, pk):
    if request.POST:
        amount = request.POST["amount"]
        order = Order.objects.get(id=pk)
        transaction = Transaction.objects.create(order=order, amount=amount)
        transaction.save()
    return redirect('create_order')


def delete_trans(request, pk):
    try:
        transaction = Transaction.objects.get(id=pk)
        transaction.delete()
    except Transaction.DoesNotExist:
        transaction = None
    return redirect('create_order')


def add_item(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        order = None
    if not order.complete:
        pk = 0

    if request.POST and order:
        item_id = request.POST['item_id']
        product_id = request.POST['product_id']
        package_id = request.POST['package']
        day = request.POST['day']
        time = request.POST['time']
        leg = request.POST['leg']
        shoulder = request.POST['shoulder']
        discount = request.POST['discount']

        if not time == "":
            try:
                time = Time.objects.get(id=time)
            except Time.DoesNotExist:
                time = None
        else:
            time = None

        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            package = None

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            product = None

        if product and package:
            if not product.category == package.category:
                return redirect('create_order', pk=pk)

        if product or package:
            try:
                order_item = OrderItem.objects.get(id=item_id)
                if order_item.delivered:
                    return redirect('create_order', pk=pk)
                if order_item.product:
                    if not order_item.product.id == product_id:
                        product1 = Product.objects.get(
                            id=order_item.product.id)
                        product1.quantity += 1
                        product1.available = True
                        product1.save()
            except OrderItem.DoesNotExist:
                order_item = OrderItem(order=order)
            if product:
                if product.quantity < order_item.quantity:
                    return redirect('create_order', pk=pk)
            order_item.package = package
            order_item.product = product
            order_item.day = day
            order_item.time = time
            order_item.leg = leg
            order_item.shoulder = shoulder
            order_item.discount = discount
            if product:
                order_item.price = product.price
                order_item.category = product.category
                if not product.quantity == 0:
                    product.quantity -= 1
                if product.quantity == 0:
                    product.available = False
                product.save()
            if package:
                order_item.price = package.price
                order_item.category = package.category
            order_item.save()
        print("Item Saved")
        return redirect('create_order', pk=pk)


@login_required(login_url='login')
def update_item(request):
    data = json.loads(request.body)
    item_id = data['itemId']
    action = data['action']

    try:
        order_item = OrderItem.objects.get(id=item_id)
    except OrderItem.DoesNotExist:
        order_item = None
    if order_item:
        if 'delete' in action:
            if order_item.product:
                product = Product.objects.get(id=order_item.product.id)
                product.quantity += order_item.quantity
                product.available = True
                product.save()
            order_item.delete()
            return JsonResponse('Item was deleted', safe=False)
        elif 'add' in action:
            if order_item.product:
                product = Product.objects.get(id=order_item.product.id)
                if product.quantity > 0:
                    order_item.quantity += 1
                    product.quantity -= 1
                    if product.quantity == 0:
                        product.available = False
                    product.save()
            else:
                if order_item.quantity < order_item.category.quantity:
                    order_item.quantity += 1
            order_item.save()
        elif 'remove' in action:
            if order_item.product:
                product = Product.objects.get(id=order_item.product.id)
                product.quantity += 1
                product.available = True
                product.save()
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity == 0:
                order_item.delete()

        elif 'edit' in action:
            if order_item.product:
                token = order_item.product.token
            else:
                token = None
            response = {
                "order_item": model_to_dict(order_item),
                "product_token": token
            }
            return JsonResponse(response, safe=False)
    return JsonResponse("no action", safe=False)
