from django.contrib import admin
from .models import CustomUser, Task
from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.contrib.admin.widgets import AdminSplitDateTime

# Register your models here.

class TaskFormNormalUser(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'timeToSend', 'owner')
        widgets = {
            'timeToSend': AdminSplitDateTime(),
        }


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ['groups', 'user_permissions']
    list_display = ('username', 'role',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'timeToSend')

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['owner'].queryset = CustomUser.objects.filter(
                username=request.user.username)
        return super(TaskAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_changeform_initial_data(self, request):
        data = super(TaskAdmin, self).get_changeform_initial_data(request)
        return data

    def get_queryset(self, request):
        qs = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
