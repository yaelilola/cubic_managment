from django.db import models
from custom_user.models import CustomUser,Unit
from facilities.models import Cubic
# Create your models here.


class AssignUserCubic(models.Model):
    assigner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='+') #TODO: type should be focal point or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='+')
    cubic = models.ForeignKey(Cubic,  on_delete=models.CASCADE)

    class Meta:
        unique_together = (("assigned_user", "cubic"),)


class Request(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='+')
    size = models.PositiveIntegerField()
    unit_near_by = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='+')
    near_lab = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    destination_date = models.DateField(null=True, blank=True)
