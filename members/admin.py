from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member


class MemberAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff")
    search_fields = (
        "username",
        "email",
    )


admin.site.register(Member, MemberAdmin)
