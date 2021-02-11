from django.contrib import admin
from .models import CustomUser,Task
# Register your models here.


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    filter_horizontal = ['groups','user_permissions']
    list_display = ('username','role',)
    exclude=('user_permissions',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
   list_display= ('title','owner','timeToSend') 