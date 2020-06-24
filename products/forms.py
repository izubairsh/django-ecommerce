from django.forms import CharField, ModelForm
from .models import Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        exclude = ('deleted', 'quantity', 'available')

    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
