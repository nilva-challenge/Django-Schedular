from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'permissions', 'email'),
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('permissions',),
        }),
    )

# admin.site.register(CustomUser, CustomUserAdmin)
# Register your custom user model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
# Register your custom user model with the default UserAdmin
# admin.site.register(CustomUser, UserAdmin)