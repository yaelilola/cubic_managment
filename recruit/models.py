from django.db import models
from custom_user.models import BusinessGroup
MAX_LENGTH = 100


class NewPosition(models.Model):
    id = models.UUIDField(primary_key=True)
    percentage = models.CharField(choices=(('full_time', 'full_time'), ('part_time', 'part_time')), max_length=MAX_LENGTH)
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
