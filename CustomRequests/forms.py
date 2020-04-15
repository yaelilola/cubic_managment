from django.forms import ModelForm
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest


class RequestToChangeCubicForm(ModelForm):
    class Meta:
        model = RequestToChangeCubic
        fields = ['cubic', 'reason']


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
    class Meta:
        model = FocalPointRequest
        fields = ['business_group', 'size', 'business_group_near_by', 'near_lab', 'near_conference_room',
                  'destination_date']


class FocalPointRequestSpacePlannerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FocalPointRequestSpacePlannerForm, self).__init__(*args, **kwargs)
        self.fields['focal_point'].widget.attrs['disabled'] = True
        self.fields['business_group'].widget.attrs['disabled'] = True
        self.fields['size'].widget.attrs['disabled'] = True
        self.fields['business_group_near_by'].widget.attrs['disabled'] = True
        self.fields['near_lab'].widget.attrs['disabled'] = True
        self.fields['near_conference_room'].widget.attrs['disabled'] = True
        self.fields['date'].widget.attrs['disabled'] = True
        self.fields['destination_date'].widget.attrs['disabled'] = True

    class Meta:
        model = FocalPointRequest
        fields = ['focal_point', 'business_group', 'size', 'business_group_near_by', 'near_lab',
                  'near_conference_room', 'date', 'destination_date', 'status', 'notes']
