from django.db import models
from employees.models import Employee


class Job(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    day1_rate = models.IntegerField()
    day2_rate = models.IntegerField()
    day3_rate = models.IntegerField()
    day1_count = models.IntegerField(default=0, null=True, blank=True)
    day2_count = models.IntegerField(default=0, null=True, blank=True)
    day3_count = models.IntegerField(default=0, null=True, blank=True)
    advance = models.IntegerField(default=0, null=True, blank=True)
    balance = models.IntegerField(default=0, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.employee.name

    @property
    def get_total(self):
        total1 = self.day1_rate * self.day1_count
        total2 = self.day2_rate * self.day2_count
        total3 = self.day3_rate * self.day3_count
        total = total1+total2+total3
        return total
