from django.forms import CharField, ModelForm
from .models import Package


class PackageForm(ModelForm):

    class Meta:
        model = Package
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
