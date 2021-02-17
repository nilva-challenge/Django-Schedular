from django.contrib.auth.admin import UserAdmin, UserCreationForm
from django.contrib import admin

from users.models import Member


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "email", "first_name", "last_name", "is_staff", )


@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    ordering = ('last_name', 'first_name')
    search_fields = ('first_name', 'last_name', 'email')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_staff'),
        }),
    )
    add_form = CustomUserCreationForm
    list_per_page = 20

    # Staffs which are not superusers can't view and edit other staffs
    def get_queryset(self, request):
        qs = super(MemberAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_staff=False)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        form = super().get_form(request, obj, **defaults)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        # Prevent non-super_users to add another super_user or admin
        # and to change user permissions and groups
        if not is_superuser:
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
