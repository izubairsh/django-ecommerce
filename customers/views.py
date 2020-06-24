from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Customer
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    q = ''
    customers = Customer.objects.order_by(
        '-date_created').filter(deleted=False)
    if 'q' in request.GET:
        q = request.GET['q']
        customers = customers.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(address__icontains=q)
        ).distinct()

    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    paged_customers = paginator.get_page(page)
    context = {
        'customers': paged_customers,
        'query': q
    }
    return render(request, 'customers/index.html', context)


@login_required(login_url='login')
def customer(request, pk):
    q = ''
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all().order_by('-date_ordered')
    total_orders = orders.count()
    if 'q' in request.GET:
        q = request.GET['q']
        orders = orders.filter(
            Q(date_created__icontains=q) |
            Q(id__icontains=q)
        ).distinct()
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'customer': customer,
        'orders': paged_orders,
        'total_orders': total_orders,
        'query': q
    }
    return render(request, 'customers/customer.html', context)


@login_required(login_url='login')
def customer_form(request, pk=0):
    if request.method == "POST":
        if pk == 0:
            phone = request.POST['phone']
            try:
                c = Customer.objects.get(phone=phone)
                c.deleted = False
                c.save()
            except Customer.DoesNotExist:
                c = None
            if c:
                form = CustomerForm(request.POST, instance=c)
            else:
                form = CustomerForm(request.POST)

        else:
            customer = Customer.objects.get(id=pk)
            form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        if pk == 0:
            form = CustomerForm()
        else:
            customer = Customer.objects.get(id=pk)
            form = CustomerForm(instance=customer)
        return render(request, "customers/customer_form.html", {'form': form})

    return render(request, "customers/customer_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.deleted = True
    customer.save()
    return redirect('customers')
