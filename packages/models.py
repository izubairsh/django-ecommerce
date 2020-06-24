import datetime
from django.db import models
from products.models import Category


class Package(models.Model):
    name = models.CharField(max_length=200)
    min_weight = models.IntegerField()
    max_weight = models.IntegerField()
    min_meat = models.IntegerField()
    max_meat = models.IntegerField()
    price = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
