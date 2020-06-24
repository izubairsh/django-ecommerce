from django.forms import CharField, ModelForm
from .models import Employee


class EmployeeForm(ModelForm):
    phone = CharField(min_length=11)
    cnic = CharField(min_length=13)

    class Meta:
        model = Employee
        fields = [
            'name',
            'phone',
            'cnic'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
