from django.db import models
from custom_user.models import CustomUser, BusinessGroup

#from django.contrib.postgres.fields import ArrayField
# Create your models here.

#
# class FocalPoint(models.Model):
#     custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
# #     # cubics = ArrayField(base_field=Cubic)
# #
# #     # def get_cubics(self):
# #     #     return self.cubics
# #     #
# #     # def set_cubics(self):
# #     #     pass
#     def __str__(self):
#         return self.custom_user.__str__()


class Request(models.Model):
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    size = models.PositiveIntegerField()
    business_group_near_by = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    near_lab = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    destination_date = models.DateField(null=True, blank=True)
