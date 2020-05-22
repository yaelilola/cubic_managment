from django.contrib import admin

# Register your models here.
from .models import Cubic, Space, Campus, Building, Floor, Lab

admin.site.register(Cubic)
admin.site.register(Space)
admin.site.register(Campus)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Lab)

