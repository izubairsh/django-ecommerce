import json
from .models import Order


def cart_data(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        order = {}
        items = {}

    return {'cart_items': cart_items, 'order': order, 'items': items}
