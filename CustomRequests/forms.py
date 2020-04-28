from django.forms import ModelForm
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from django import forms
from facilities.models import Cubic,Space


class RequestToChangeCubicForm(forms.Form):
    cubic = forms.ModelChoiceField(queryset=Cubic.objects.all(), required=False)
    reason = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, cubics_queryset, **kwargs):
        super(RequestToChangeCubicForm, self).__init__(*args, **kwargs)
        self.fields['cubic'].queryset = cubics_queryset


class RequestToChangeCubicFocalPointForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestToChangeCubicFocalPointForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['disabled'] = True
        self.fields['request_date'].widget.attrs['readonly'] = True
        self.fields['cubic'].widget.attrs['disabled'] = True
        self.fields['reason'].widget.attrs['readonly'] = True

    class Meta:
        model = RequestToChangeCubic
        fields = ['user', 'request_date', 'cubic', 'reason', 'status', 'notes']


class FocalPointRequestForm(ModelForm):
    def __init__(self, *args, business_group_qs, **kwargs):
        super(FocalPointRequestForm, self).__init__(*args, **kwargs)
        self.fields['near_lab'].queryset = Space.objects.filter(type='Lab')
        self.fields['business_group_near_by'].queryset = business_group_qs

    class Meta:
        model = FocalPointRequest
        fields = ['part_time_employees_amount', 'full_time_employees_amount', 'business_group_near_by', 'near_lab',
                  'destination_date']


class FocalPointRequestSpacePlannerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FocalPointRequestSpacePlannerForm, self).__init__(*args, **kwargs)
        self.fields['business_group'].widget.attrs['disabled'] = True
        self.fields['part_time_employees_amount'].widget.attrs['disabled'] = True
        self.fields['full_time_employees_amount'].widget.attrs['disabled'] = True
        self.fields['business_group_near_by'].widget.attrs['disabled'] = True
        self.fields['near_lab'].widget.attrs['disabled'] = True
        self.fields['date'].widget.attrs['disabled'] = True
        self.fields['destination_date'].widget.attrs['disabled'] = True

    class Meta:
        model = FocalPointRequest
        fields = ['business_group', 'part_time_employees_amount', 'full_time_employees_amount', 'business_group_near_by',
                  'near_lab', 'date', 'destination_date', 'status', 'notes']
