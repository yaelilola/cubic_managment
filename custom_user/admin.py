from django.contrib import admin

# Register your models here.

from .models import Group, CustomUser

admin.site.register(Group)
admin.site.register(CustomUser)
admin.site.register(AssignUserCubic)
admin.site.register(AssignGroupCubic)
