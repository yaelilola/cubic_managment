from django.db import models
from custom_user.models import BusinessGroup
from django.utils.timezone import now
MAX_LENGTH = 100


class NewPosition(models.Model):
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE)
    creation_date = models.DateField(default=now, null=True, blank=True)
    college_graduate_internal_and_external = models.IntegerField()
    experienced_internal_and_external = models.IntegerField()
    intel_contract_employee_internal_and_external = models.IntegerField()
    student_intern_internal_and_external = models.IntegerField()
    technical_graduate_internal_and_external = models.IntegerField()
    college_graduate_internal_only = models.IntegerField()
    experienced_internal_only = models.IntegerField()
    intel_contract_employee_internal_only = models.IntegerField()
    student_intern_internal_only = models.IntegerField()
    technical_graduate_internal_only = models.IntegerField()
