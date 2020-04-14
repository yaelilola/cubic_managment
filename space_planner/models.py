from django.db import models
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic

# Create your models here.


class AssignGroupCubic(models.Model):
    assigner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')  # TODO: type should be space planner or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    cubic = models.ForeignKey(Cubic, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("cubic", "assigned_business_group"),)
