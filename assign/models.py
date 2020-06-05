from django.db import models
from facilities.models import Cubic
from custom_user.models import CustomUser
from django.utils import timezone

# Create your models here.


class AssignUserCubic(models.Model):
    time = models.DateField(null=True, blank=True, default=timezone.now())
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cubic = models.ForeignKey(Cubic, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("assigned_user", "cubic"),)



