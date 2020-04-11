from django.contrib import admin

# Register your models here.
from .models import Cubic, Space, Campus, Site, Floor

admin.site.register(Cubic)
admin.site.register(Space)
admin.site.register(Campus)
admin.site.register(Site)
admin.site.register(Floor)

