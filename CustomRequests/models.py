from django.db import models
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic
from django.utils.timezone import now
from focal_point.models import FocalPoint
MAX_LENGTH = 100

# Create your models here.
class RequestToChangeCubic(models.Model):
    #id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_date = models.DateField(default=now())
    cubic = models.ForeignKey(Cubic, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=MAX_LENGTH, choices=(('unread', 'unread'), ('in progress', 'in progress'),
                                                              ('approved', 'approved'), ('denied', 'denied')),
                              default='unread')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    #TODO: add conversation field


class FocalPointRequest(models.Model):
    focal_point = models.ForeignKey(FocalPoint, on_delete=models.CASCADE)
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+')
    size = models.PositiveIntegerField()
    business_group_near_by = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, related_name='+',
                                               blank=True, null=True)
    near_lab = models.BooleanField(default=False)
    near_conference_room = models.BooleanField(default=False)
    date = models.DateField(default=now())
    destination_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=MAX_LENGTH, choices=(('unread', 'unread'), ('in progress', 'in progress'),
                                                              ('approved', 'approved'), ('denied', 'denied')),
                              default='unread')
    notes = models.TextField(blank=True)
    # TODO: add conversation field
