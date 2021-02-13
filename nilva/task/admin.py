from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    def has_view_permission(self, request,obj=None):
        return True

    def has_module_permission(self,request):
        return True

    def has_edit_permission(self,request):
        return True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request,obj=None):
        return True

    def get_queryset(self, request):
        user=request.user
        if user.is_superuser==True:
            return Task.objects.all()
        else:
            return Task.objects.all().filter(owner_id=user.id)
        #return super().get_queryset(request)
            



admin.site.register(Task,TaskAdmin)

'''


'''