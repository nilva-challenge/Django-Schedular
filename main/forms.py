from django import forms
from main.models import Task, User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets 
from datetime import datetime, timezone


class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','permission']


class TaskCreateForm(ModelForm):
    
    time_to_send = forms.DateTimeField(
        widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}))
    
    class Meta:
        model = Task
        fields = ['title','description','time_to_send','precondition_tasks']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        if self.request.user.permission == 'A':
            self.fields['owner']=forms.ModelChoiceField(queryset=User.objects.all())

    def init_owner(self, request, obj):
        if request.user.permission == 'A':
            owner_id = obj.owner.id
            user = User.objects.get(id=owner_id)
            self.fields['owner'].initial = user

    def validation(self, request):
        obj = self.save(commit=False) 
        precondition_tasks = self.cleaned_data['precondition_tasks']

        if obj.time_to_send <= datetime.now(timezone.utc):
            raise forms.ValidationError("the time to send of task is not valid")
        
        for pre_task in precondition_tasks:
            if pre_task.time_to_send >= obj.time_to_send:
                raise ValidationError(
                    "the time to send of task is not valid " +
                    "(time to send of task most be greater than precondition tasks time to send )"
                )
        if request.user.permission == 'N':
            obj.owner = request.user
        else:
            obj.owner = self.cleaned_data['owner']
        obj.save()
    