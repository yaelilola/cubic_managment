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
        if len(AssignUserCubic.objects.filter(cubic=cubic))+person_amount <= 2:
            return True
        else:
            return False


def get_available_cubics(business_group, person_amount=1, cubic_type='private'):
    print(cubic_type)
    cubics_queryset_aux = list(Cubic.objects.filter(business_group=business_group, type=cubic_type))
    print(len(cubics_queryset_aux))
    avail_cubics = []
    for cubic in cubics_queryset_aux:
        if is_cubic_available(cubic, person_amount)is True:
            avail_cubics.append(cubic)
    print(len(avail_cubics))
    limited_cubics = avail_cubics[:999]
    limited_cubics_ids = [cubic.id for cubic in limited_cubics]
    cubics_queryset = Cubic.objects.filter(id__in=limited_cubics_ids)
    return cubics_queryset


class AssignPartTimeUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), to_field_name="employee_number")
    cubics = forms.ModelMultipleChoiceField(queryset=Cubic.objects.none())

    def __init__(self, users_queryset, business_group, *args, **kwargs):
        super(AssignPartTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = get_available_cubics(business_group, 1, 'shared')


class AssignFullTimeUserCubicForm(forms.Form):
    users = forms.ModelChoiceField(queryset=CustomUser.objects.all(), to_field_name="employee_number", widget=autocomplete.ModelSelect2(url='custom_user:customuser-autocomplete',
                                                                   attrs={'data-placeholder': 'Type the user name ...','data-html': True}))
    cubics = forms.ModelChoiceField(queryset=Cubic.objects.none())

    def __init__(self, users_queryset, business_group, *args, **kwargs):
        super(AssignFullTimeUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['cubics'].queryset = get_available_cubics(business_group, 1, 'private')


class AssignSpacesToBusinessGroupsForm(forms.Form):
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.filter(admin_group=False))
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all())









