from assign.models import AssignUserCubic
from custom_user.models import CustomUser
from focal_point.models import FocalPoint
from facilities.models import Cubic
from django import forms


class AssignUserCubicForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.focal_point = kwargs.pop('focal_point')
        super(AssignUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(CustomUser.objects.filter(business_group=self.focal_point.custom_user.business_group))
        self.fields['cubics'] = forms.ModelMultipleChoiceField(Cubic.objects.filter(focal_point=self.focal_point))






