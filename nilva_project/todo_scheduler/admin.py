from django.contrib import admin
from .models import Todo

# Register your models here.

class TodoAdmin(admin.ModelAdmin):

    list_display = ("__str__","owner","date")
    
    # allow usser just access to his/her own objects
    def get_queryset(self, request):
        qs = super(TodoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_add_permission(self,request):
        return True

    def has_change_permission(self,request,obj=None):
        return True

    def has_view_permission(self,request,obj=None):
        return True

    def has_module_permission(self,request,obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    # dont allow current_user to create object for another 
    exclude = ('owner',)
    def save_model( self, request, obj, form, change ):
        obj.owner = request.user
        obj.save()

    

admin.site.register(Todo,TodoAdmin)