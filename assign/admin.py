from django.contrib import admin
from .models import AssignUserCubic

admin.site.register(AssignUserCubic)

list_display = ('assigner', 'time', 'assigned_user', 'cubic')