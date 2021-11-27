from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm,widgets
from .models import Task
from django import forms

class Taskform(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'pre_tasks' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(Taskform, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        self.fields['timeToSend'].widget.attrs.update({'class' : 'input' , 'placeholder':'d/m/y H:M:S'})