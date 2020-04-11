from django.forms import ModelForm
from .models import CustomUser


class CustomUserSignUpForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['employee_number', 'password', 'type', 'start_date', 'end_date', 'percentage', 'group']

