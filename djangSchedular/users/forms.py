from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm,widgets
from .models import Profile
from django import forms





class Userform(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'