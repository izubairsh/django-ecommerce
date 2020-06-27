from django.db import models
from products.models import Product, Category
from orders.models import Order
from packages.models import Package

DAY_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
)

COUNT_CHOICES = (
    ('1', '1'),
    ('2', '2')
)


class Time(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, null=True, blank=True)
    package = models.ForeignKey(
        Package, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.IntegerField(default=1,)
    price = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    day = models.CharField(choices=DAY_CHOICES,
                           max_length=1, null=True, blank=True)
    time = models.ForeignKey(
        Time, on_delete=models.PROTECT, null=True, blank=True)
    leg = models.CharField(max_length=1, null=True, blank=True)
    shoulder = models.CharField(max_length=1, null=True, blank=True)

    discount = models.IntegerField(default=0, null=True, blank=False)
    complete = models.BooleanField(default=False)
    processing = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total-self.discount

    class Meta:
        ordering = ['-id']
