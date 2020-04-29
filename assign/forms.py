from assign.models import AssignUserCubic
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic, Space
from django import forms
from django.db import models


class AssignPartTimeUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), to_field_name="email")
    cubics = forms.ModelMultipleChoiceField(queryset=Cubic.objects.all())

    def __init__(self, users_queryset, cubics_queryset, *args, **kwargs):
        super(AssignPartTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = cubics_queryset


class AssignFullTimeUserCubicForm(forms.Form):
    users = forms.ModelChoiceField(queryset=CustomUser.objects.all(),to_field_name="email")
    cubics = forms.ModelChoiceField(queryset=Cubic.objects.all())

    def __init__(self, users_queryset, cubics_queryset, *args, **kwargs):
        super(AssignFullTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = cubics_queryset


class AssignSpacesToBusinessGroupsForm(forms.Form):
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all())
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.filter(admin_group=False))








