from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'time_to_send')
    ordering = ('time_to_send', 'title')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('owner', 'time_to_send')
    list_per_page = 20


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


user_site.register(Task, TaskUser)
