from django.forms import CharField, ModelForm
from .models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
