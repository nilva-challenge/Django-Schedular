from django.contrib import admin
from .models import Task
from .tasks import send_task_mail
from celery import shared_task
from celery.app.control import Control
from ch_nilva.celery import app


@admin.register(Task)
class CustomTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_to_send',)
    list_filter = ('time_to_send', 'owner',)
    search_fields = ('owner', 'title',)

    # exclude = ('celery_task_id',)

    def get_queryset(self, request):
        qs = super(CustomTaskAdmin, self).get_queryset(request)
        if not request.user.is_admin:
            return qs.filter(owner=request.user)
        return qs

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return super(CustomTaskAdmin, self).has_change_permission(request, obj)
        return request.user.is_admin or request.user.is_superuser

    def get_form(self, request, obj=None, change=False, **kwargs):
        user = request.user
        form = super(CustomTaskAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['celery_task_id'].disabled = True
        if (not user.is_admin) and (not user.is_superuser):
            form.base_fields['owner'].initial = user
            form.base_fields['owner'].disabled = True
            return form
        else:
            form.base_fields['owner'].diabled = False
            return form

    def save_model(self, request, obj, form, change):
        # changed data
        if change:
            if 'time_to_send' in form.changed_data:
                task_obj = Task.objects.get(id=obj.id)
                control = Control(app)
                control.terminate(task_id=task_obj.celery_task_id)
                id = send_task_mail.apply_async(args=[task_obj.owner.email])
                obj.celery_task_id = id
            super(CustomTaskAdmin, self).save_model(request, obj, form, change)

        # new task added
        else:
            email = obj.owner.email
            time_to_send = obj.time_to_send
            # send_task_mail(email)
            id = send_task_mail.apply_async(args=[email])
            obj.celery_task_id = id
            super(CustomTaskAdmin, self).save_model(request, obj, form, change)
        super(CustomTaskAdmin, self).save_model(request, obj, form, change)
