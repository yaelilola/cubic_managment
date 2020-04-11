from django.contrib import admin

# Register your models here.

from .models import Group, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    #TODO: showing only relevant fields
    #exclude = ('last_login', 'is_superuser', 'groups', 'user_permission', 'is_staff', 'is_active', 'date_joined')
    fields = ('password','username','first_name','last_name','email','employee_number','type','start_date','end_date', 'percentage','group')


admin.site.register(Group)
admin.site.register(CustomUser)
