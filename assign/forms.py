from assign.models import AssignUserCubic
from custom_user.models import CustomUser
from focal_point.models import FocalPoint
from facilities.models import Cubic
from django import forms
from django.db import models


class AssignUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())
    cubics = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, users_queryset, cubics_queryset, *args, **kwargs):
        super(AssignUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = cubics_queryset








