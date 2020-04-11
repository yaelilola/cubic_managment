from django.contrib import admin
from custom_user.forms import CustomUserSignUpForm
# Register your models here.

from custom_user.models import Group, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    #TODO: showing only relevant fields
    add_form = CustomUserSignUpForm
    model = CustomUser
    #exclude = ('last_login', 'is_superuser', 'groups', 'user_permission', 'is_staff', 'is_active', 'date_joined')
    list_display = ['password','username','first_name','last_name','email','employee_number','type','start_date','end_date', 'percentage','group']


admin.site.register(Group)
admin.site.register(CustomUser)
