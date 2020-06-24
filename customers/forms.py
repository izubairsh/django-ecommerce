from django.forms import CharField, ModelForm
from .models import Customer


class CustomerForm(ModelForm):
    phone = CharField(min_length=11)

    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'address'
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
