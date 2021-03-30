from django.contrib import admin
from .models import User
from schedule.models import Task
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode


@admin.register(User)
class CustomAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_fullname', 'is_admin', 'is_superuser', 'get_link_owner_task')
    list_filter = ('username', 'email', 'is_admin',)

    def get_link_owner_task(self, obj):
        count = len(Task.objects.filter(owner=obj))
        url = (
                reverse("admin:schedule_task_changelist")
                + '?'
                + urlencode({"owner__id__exact": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Tasks</a>', url, count)

    get_link_owner_task.short_description = 'Tasks'

    def get_fullname(self, obj):
        return obj.first_name + ' ' + obj.last_name

    get_fullname.short_description = 'Full Name'

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_admin

    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin or request.user.is_superuser

    def get_queryset(self, request):
        qs = super(CustomAccountAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_admin:
            qs = qs.filter(is_superuser=False)
            return qs
        return qs.filter(username=request.user.username)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = ()
        elif request.user.is_admin:
            self.exclude = ('is_superuser', 'user_permissions', 'groups', 'is_staff', 'is_active')
        return super(CustomAccountAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = ()
        elif request.user.is_admin:
            self.exclude = ('is_superuser', 'user_permissions', 'groups', 'is_staff', 'is_active')
        return super(CustomAccountAdmin, self).change_view(request, object_id, form_url, extra_context)
