from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order_items.models import OrderItem


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
    items = OrderItem.objects.all().filter(product=None)

    context = {
        'sales': 112,
        'revenue': 3234,
        'cost': 234,
        'profit': 3000,
        'items': items,
    }
    return render(request, 'dashboard.html', context)
