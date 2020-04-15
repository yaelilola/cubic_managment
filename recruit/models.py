from django.db import models
from custom_user.models import BusinessGroup
from django.utils.timezone import now
MAX_LENGTH = 100


class NewPosition(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, blank=True)
    percentage = models.CharField(choices=(('full_time', 'full_time'), ('part_time', 'part_time')), max_length=MAX_LENGTH)
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE)
    creation_date = models.DateField(default=now)

    def __str__(self):
        return self.name
