from assign.models import AssignUserCubic
from custom_user.models import CustomUser
from facilities.models import Cubic
from django import forms


def convert_to_2tuple(data):
    ret_val = []
    for item in data:
        new_tuple = (str(item), str(item))
        ret_val.append(new_tuple)
    return iter(ret_val)

class AssignUserCubicForm(forms.Form):
    users = forms.MultipleChoiceField(choices=convert_to_2tuple(CustomUser.objects.all()))
    cubics = forms.MultipleChoiceField(choices=convert_to_2tuple(Cubic.objects.all()))
