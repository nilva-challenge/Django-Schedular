from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from users.models import Member
from .models import Task
from .tasks import send_scheduled_mail


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'view_owner_link', 'time_to_send')
    ordering = ('time_to_send', 'title')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('owner', 'time_to_send')
    list_per_page = 20

    def view_owner_link(self, obj):
        url = (
            reverse('admin:users_member_change', args=[obj.owner_id])
            + '?'
            + urlencode({'tasks__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, obj.owner)

    view_owner_link.short_description = 'Owner'

    def save_model(self, request, obj, form, change):
        time_to_send = obj.time_to_send
        email = obj.owner.email
        send_scheduled_mail.apply_async(args=[email], eta=time_to_send)
        super().save_model(request, obj, form, change)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['owner'].queryset = Member.objects.filter(is_staff=False)
        return super(TaskAdmin, self).render_change_form(request, context, *args, **kwargs)


# django admin interface authentication for non-staff members
# for the new instance of AdminSite
class UserAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password for a user "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


# New instance of AdminSite for non-staff users
class UserSite(AdminSite):
    login_form = UserAuthenticationForm

    def has_permission(self, request):
        return request.user.is_active and not request.user.is_staff


user_site = UserSite(name='user_interface')


class TaskUser(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'time_to_send')
    ordering = ('time_to_send', 'title')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('time_to_send',)
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(TaskUser, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        time_to_send = obj.time_to_send
        email = obj.owner.email
        send_scheduled_mail.apply_async(args=[email], eta=time_to_send)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return ['owner', ]


user_site.register(Task, TaskUser)
