from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import OrderItem
import datetime
from packages.models import Package
import array as arr
# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.POST:
        item_id = request.POST['id']
        try:
            item = OrderItem.objects.get(id=item_id)
        except OrderItem.DoesNotExist:
            item = None
        if item:
            status = request.POST['status']
            if status == 'complete':
                item.delivered = True
                item.complete = False
            item.save()
    q = ''
    day = '1'
    status = 'complete'
    if 'day' in request.GET:
        day = request.GET['day']

    if 'status' in request.GET:
        status = request.GET['status']
    if status == 'complete':
        items = OrderItem.objects.order_by(
            'time').filter(complete=True, day=day)
    elif status == 'delivered':
        items = OrderItem.objects.order_by(
            'time').filter(delivered=True, day=day)

    packages = Package.objects.all()
    total = []

    for package in packages:
        count = items.filter(package=package, product=None).count()
        total.append({
            "name": package.name,
            "count": count
        })
    items = items.exclude(package=None)
    items_count = items.count()
    items = items.filter(day=day)
    if 'q' in request.GET:
        q = request.GET['q']
        if not q == '':
            items = items.filter(order=q).distinct()

    paginator = Paginator(items, 15)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)
    context = {
        'items': paged_items,
        'query': q,
        'day': day,
        'status': status,
        'packages': total,
        'items_count': items_count
    }
    return render(request, 'order_items/index.html', context)
