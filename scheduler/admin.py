from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from members.models import Member
from scheduler.models import Task
from django import forms


def get_form_class_with_request(
    form_class: type[forms.ModelForm], request: HttpRequest
):
    def init_form(*args, **kwargs) -> forms.ModelForm:
        kwargs.update({"current_user": request.user})
        form_instance = form_class(*args, **kwargs)

        return form_instance

    init_form.base_fields = form_class.base_fields

    return init_form


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "owner",
            "time_to_send",
            "precondition_tasks",
        ]
        widgets = {
            "precondition_tasks": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user")
        super().__init__(*args, **kwargs)
        if not current_user.is_superuser:
            self.fields["precondition_tasks"].queryset = Task.objects.filter(
                owner=current_user
            )
            self.fields["owner"].initial = current_user
            self.fields["owner"].disabled = True


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ["title", "description", "owner", "time_to_send"]
    list_filter = ["owner"]

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form_proxy = get_form_class_with_request(form, request)

        return form_proxy

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.has_perm(
            "scheduler.view_task"
        ):
            qs = qs.filter(owner=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner" and not request.user.is_superuser:
            kwargs["queryset"] = Member.objects.filter(
                username=request.user.username
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.owner == request.user:
            return True
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and obj.owner == request.user:
            return True
        return super().has_change_permission(request, obj)


admin.site.register(Task, TaskAdmin)
