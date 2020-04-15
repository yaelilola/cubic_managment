from django.db import models
from facilities.models import Cubic
from focal_point.models import FocalPoint
from custom_user.models import CustomUser
from django.utils import timezone

# Create your models here.


class AssignUserCubic(models.Model):
    assigner = models.ForeignKey(FocalPoint, on_delete=models.CASCADE, related_name='+')  #TODO: type should be focal point or higher?
    time = models.DateField(null=True, blank=True, default=timezone.now())
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    cubic = models.ForeignKey(Cubic, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("assigned_user", "cubic"),)

    def __str__(self):
        return self.assigned_user.__str__()


