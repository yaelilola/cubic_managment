from django.db import models
from django.contrib.auth.models import User
from facilities.models import Cubic


class Group(models.Model):
    id = models.UUIDField(primary_key=True)

    def __str__(self):
        return self.id


class CustomUser(User):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(choices=(('regular','regular'),('space_planner','space_planner'),('focal_point','focal_point')))
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    percentage = models.CharField(choices=(('full_time','full_time'),('part_time','part_time')))
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # class Meta:
    #      proxy = True
    #      ordering = ('first_name', )

    def __str__(self):
        return self.username

