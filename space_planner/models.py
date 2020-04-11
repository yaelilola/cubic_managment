from django.db import models
from custom_user.models import CustomUser, Group
from facilities.models import Cubic

# Create your models here.


class AssignGroupCubic(models.Model):
    assigner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # TODO: type should be space planner or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_group = models.ForeignKey(Group, on_delete=models.CASCADE, primary_key=True)
    cubic = models.ForeignKey(Cubic, on_delete=models.CASCADE, primary_key=True)
