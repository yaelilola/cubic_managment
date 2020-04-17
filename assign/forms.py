from assign.models import AssignUserCubic
from custom_user.models import CustomUser, BusinessGroup
from focal_point.models import FocalPoint
from facilities.models import Cubic, Space
from django import forms
from django.db import models


class AssignUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())
    cubics = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, *args, users_queryset, cubics_queryset, **kwargs):
        super(AssignUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = cubics_queryset


class AssignSpacesToBusinessGroupsForm(forms.Form):
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all())
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.all())
    # business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE)








