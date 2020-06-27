from django.db import models


class Expense(models.Model):
    name = models.CharField(max_length=10)
    amount = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=10)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-id']
