from django.forms import ModelForm
from CustomRequests.models import RequestToChangeCubic

class RequestToChangeCubicForm(ModelForm):
    class Meta:
        model = RequestToChangeCubic
        fields = ['cubic', 'reason']