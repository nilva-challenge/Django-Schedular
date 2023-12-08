from django.contrib import admin

from core.users.models import User
from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ("-created",)
    list_filter = ("owner",)
    list_display = [
        "title",
        "owner",
        "send_time_schedule",
        "send_time_done",
        "parent",
    ]
    search_fields = [
        "id",
        "title",
        "owner__username",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
        "description",
    ]

    def get_form(self, request, obj=None, **kwargs):
        user = request.user
        form = super().get_form(request, obj, **kwargs)
        if user.groups.filter(name="User"):
            form.base_fields["owner"].queryset = User.objects.filter(id=user.id)
        return form

    def get_queryset(self, request):
        if request.user.groups.filter(name="User"):
            return super().get_queryset(self).filter(owner=request.user)
        return super().get_queryset(self)
