from django.contrib import admin
from .models import Task
from .tasks import send_task_mail
from celery.app.control import Control
from ch_nilva.celery import app
from django.urls import reverse
from django.utils.html import format_html
from account.models import User


@admin.register(Task)
class CustomTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_to_send', 'get_task_link',)
    list_filter = ('time_to_send', 'owner',)
    search_fields = ('owner', 'title',)
    readonly_fields = ('celery_task_id',)
    actions = None

    def get_task_link(self, obj):
        username = obj.owner.username
        url = (
            reverse("admin:account_user_change", args=(obj.owner.id,))
        )
        return format_html('<a href="{}"> {} </a>', url, username)

    get_task_link.short_description = 'owner'

    def get_queryset(self, request):
        qs = super(CustomTaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_admin:
            return qs.filter(owner__is_superuser=False)
        else:
            return qs.filter(owner=request.user)

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return super(CustomTaskAdmin, self).has_change_permission(request, obj)
        return request.user.is_superuser or request.user.is_admin

    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return super(CustomTaskAdmin, self).has_change_permission(request, obj)
        return request.user.is_admin or request.user.is_superuser

    # set policy of making task for other users : normal -> normal
    # admin -> admin, normal |  superuser -> superuser, admin, normal
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        query = super(CustomTaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'owner':
            if request.user.is_superuser:
                return query
            if request.user.is_admin:
                kwargs['queryset'] = User.objects.filter(is_superuser=False)
            else:
                kwargs['queryset'] = User.objects.filter(id=request.user.id)
            return super(CustomTaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return query

    def delete_model(self, request, obj):
        """ cancel the task from broker """
        celery_task_id = obj.celery_task_id
        con = Control(app)
        con.terminate(task_id=celery_task_id)
        super(CustomTaskAdmin, self).delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        # changed data
        if change:
            if 'time_to_send' in form.changed_data:
                control = Control(app)
                control.terminate(task_id=obj.celery_task_id)
                id = send_task_mail.apply_async(args=[obj.owner.email], eta=obj.time_to_send)
                obj.celery_task_id = id
            super(CustomTaskAdmin, self).save_model(request, obj, form, change)

        # new task added
        else:
            email = obj.owner.email
            time_to_send = obj.time_to_send
            id = send_task_mail.apply_async(args=[email], eta=time_to_send)
            obj.celery_task_id = id
            super(CustomTaskAdmin, self).save_model(request, obj, form, change)
