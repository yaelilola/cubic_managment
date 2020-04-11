from django.db import models
from django.contrib.auth.models import User
from facilities.models import Cubic
MAX_LENGTH = 100

class Group(models.Model):
    id = models.CharField(primary_key=True,max_length=MAX_LENGTH)

    def __str__(self):
        return self.id


class CustomUser(User):
    employee_number = models.UUIDField(primary_key=True)
    type = models.CharField(choices=(('regular','regular'),('space_planner','space_planner'),('focal_point','focal_point')), max_length=MAX_LENGTH)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    percentage = models.CharField(choices=(('full_time','full_time'),('part_time','part_time')),max_length=MAX_LENGTH)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # class Meta:
    #      proxy = True
    #      ordering = ('first_name', )

    def create_user(self, _employee_number, _type, _percentage, _group, _start_date=None, _end_date=None):
        user = CustomUser()
        user.employee_number = _employee_number
        user.type = _type
        user.percentage = _percentage
        user.group = _group
        user.start_date = _start_date
        user.end_date = _end_date
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def __str__(self):
        return self.username

