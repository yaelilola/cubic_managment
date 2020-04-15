# from django.contrib import admin
# from custom_user.forms import CustomUserSignUpForm
# # Register your models here.
#
# from custom_user.models import Group, CustomUser
#
#
# class CustomUserAdmin(admin.ModelAdmin):
#     #TODO: showing only relevant fields
#     add_form = CustomUserSignUpForm
#     model = CustomUser
#     #exclude = ('last_login', 'is_superuser', 'groups', 'user_permission', 'is_staff', 'is_active', 'date_joined')
#     list_display = ['password','username','first_name','last_name','email','employee_number','type','start_date','end_date', 'percentage','group']

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BusinessGroup

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'employee_number', 'focal_point', 'space_planner', 'percentage',
                    'business_group', 'start_date', 'end_date')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.register(BusinessGroup)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
