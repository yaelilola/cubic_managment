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
