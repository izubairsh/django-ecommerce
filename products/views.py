from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from products.forms import ProductForm
from django.db.models import Q
from datetime import datetime


@login_required(login_url='login')
def index(request):
    q = ''
    categories = Category.objects.all()
    t = categories.first()

    today = datetime.today()
    sellectedYear = today.year
    if 'sellectedYear' in request.GET:
        sellectedYear = request.GET['sellectedYear']

    if 'type' in request.GET:
        t = Category.objects.get(name=request.GET['type'])
    products = Product.objects.order_by('-date_created').filter(category=t)
    
    if 'q' in request.GET:
        q = request.GET['q']
        products = products.filter(
            Q(token__icontains=q) |
            Q(price__icontains=q)
        ).distinct()
    products = products.filter(
        Q(date_created__icontains=sellectedYear)
    ).distinct()

    status = 'inStock'
    if 'status' in request.GET:
        status = request.GET['status']
    # if status == 'inStock':
        
    # elif status == 'expense':


    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products': paged_products,
        'query': q,
        'type': t.name,
        'categories': categories,
        'sellectedYear': sellectedYear
    }
    return render(request, 'products/index.html', context)


@login_required(login_url='login')
def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product.html', context)


@login_required(login_url='login')
def product_form(request, pk=0):
    if request.method == "POST":
        if pk == 0:
            form = ProductForm(request.POST, request.FILES)
        else:
            product = Product.objects.get(id=pk)
            form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if pk == 0:
                product.quantity = product.category.quantity
            product.save()
            return redirect('products')
    else:
        if pk == 0:
            form = ProductForm()
        else:
            product = Product.objects.get(id=pk)
            form = ProductForm(instance=product)
        return render(request, "products/product_form.html", {'form': form})

    return render(request, "products/product_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    if 'type' in request.GET:
        t = request.GET['type']
        return redirect(reverse('products') + '?type='+t)
    return redirect('products')
