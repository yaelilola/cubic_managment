from django.db import models
from custom_user.models import CustomUser, Group
from facilities.models import Cubic
# Create your models here.


class AssignUserCubic(models.Model):
    assigner = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #TODO: type should be focal point or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cubic = models.ForeignKey(Cubic,  on_delete=models.CASCADE, primary_key=True)


class Request(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()
    group_near_by = models.ForeignKey(Group, on_delete=models.CASCADE)
    near_lab = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    destination_date = models.DateField(null=True, blank=True)
