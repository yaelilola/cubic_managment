from django.db import models
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class FocalPoint(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
#     # cubics = ArrayField(base_field=Cubic)
#
#     # def get_cubics(self):
#     #     return self.cubics
#     #
#     # def set_cubics(self):
#     #     pass


class AssignUserCubic(models.Model):
    assigner = models.ForeignKey(FocalPoint, on_delete=models.CASCADE,related_name='+') #TODO: type should be focal point or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='+')
    cubic = models.ForeignKey(Cubic,  on_delete=models.CASCADE)

    class Meta:
        unique_together = (("assigned_user", "cubic"),)


class Request(models.Model):
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    size = models.PositiveIntegerField()
    business_group_near_by = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    near_lab = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    destination_date = models.DateField(null=True, blank=True)
