from assign.models import AssignUserCubic
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic, Space
from django import forms
from django.db import models

from dal import autocomplete


def is_cubic_available(cubic, person_amount=1):
    if cubic.type == 'private':
        if len(AssignUserCubic.objects.filter(cubic=cubic)) < 1 and person_amount == 1:
            return True
        else:
            return False
    else:
    #should be shared
        if len(AssignUserCubic.objects.filter(cubic=cubic))+person_amount <= cubic.capacity:
            return True
        else:
            return False


def get_available_cubics(business_group, user_current_cubic, person_amount=1, cubic_type='private'):
    cubics_queryset_aux = list(Cubic.objects.filter(business_group=business_group, type=cubic_type))
    avail_cubics = []
    for cubic in cubics_queryset_aux:
        if is_cubic_available(cubic, person_amount)is True:
            avail_cubics.append(cubic)
    limited_cubics = user_current_cubic
    limited_cubics = (avail_cubics[:(999-len(user_current_cubic)-1)])
    limited_cubics_ids = [cubic.id for cubic in limited_cubics]
    limited_cubics_ids += user_current_cubic
    cubics_queryset = Cubic.objects.filter(id__in=limited_cubics_ids)
    return cubics_queryset


class AssignPartTimeUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), to_field_name="employee_number")
    cubics = forms.ModelMultipleChoiceField(queryset=Cubic.objects.none())

    def __init__(self, users_queryset, user_current_cubic, business_group, *args, **kwargs):
        super(AssignPartTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = get_available_cubics(business_group, user_current_cubic, 1, 'shared')


class AssignFullTimeUserCubicForm(forms.Form):
    users = forms.ModelChoiceField(queryset=CustomUser.objects.none())
    cubics = forms.ModelChoiceField(queryset=Cubic.objects.none())

    def __init__(self, users_queryset, user_current_cubic, business_group, *args, **kwargs):
        super(AssignFullTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = get_available_cubics(business_group, user_current_cubic, 1, 'private')


class AssignSpacesToBusinessGroupsForm(forms.Form):
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.filter(admin_group=False))
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all())









