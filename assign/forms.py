from assign.models import AssignUserCubic
from custom_user.models import CustomUser
from facilities.models import Cubic
from django import forms


class AssignUserCubicForm(forms.Form):
    users = forms.ModelMultipleChoiceField(CustomUser.objects.all())
    cubics = forms.ModelMultipleChoiceField(Cubic.objects.all())