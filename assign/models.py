from django.db import models
from facilities.models import Cubic
from focal_point.models import FocalPoint
from custom_user.models import CustomUser
# Create your models here.


class AssignUserCubic(models.Model):
    assigner = models.ForeignKey(FocalPoint, on_delete=models.CASCADE, related_name='+')  #TODO: type should be focal point or higher?
    time = models.DateField(null=True, blank=True, auto_now_add=True)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    cubic = models.ForeignKey(Cubic,  on_delete=models.CASCADE)

    class Meta:
        unique_together = (("assigned_user", "cubic"),)


    def __str__(self):
        return self.assigned_user.__str__() + ", " + self.cubic.__str__()

