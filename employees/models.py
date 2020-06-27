from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11, unique=True)
    cnic = models.CharField(max_length=13, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
