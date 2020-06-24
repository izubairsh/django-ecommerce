from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True, blank=False)
    complete = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    date_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_discount(self):
        order_items = self.orderitem_set.all()
        total = sum([item.discount for item in order_items])
        return total

    @property
    def get_balance(self):
        transactions = self.transaction_set.all()
        total = sum([transaction.amount for transaction in transactions])
        return self.get_cart_total-total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_payable(self):
        transactions = self.transaction_set.all()
        total = sum([transaction.amount for transaction in transactions])
        order_items = self.orderitem_set.all().filter(delivered=True)
        item_total = sum([item.get_total for item in order_items])

        return total-item_total

    @property
    def get_total_paid(self):
        transactions = self.transaction_set.all()
        total = sum([transaction.amount for transaction in transactions])
        return total

    @property
    def get_status(self):
        order_items = self.orderitem_set.all()
        for item in order_items:
            if not item.delivered:
                return False
        return True


class Transaction(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT)
    amount = models.IntegerField()
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.order.id)
