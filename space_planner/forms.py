from django import forms
from custom_user.models import CustomUser, BusinessGroup


class ChooseFocalPointForm(forms.Form):
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.all())
    employee = forms.ModelChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_group'].queryset = BusinessGroup.objects.all()
        self.fields['employee'].queryset = CustomUser.objects.none()

        if 'business_group' in self.data:
            try:
                business_group = int(self.data.get('business_group'))
                self.fields['city'].queryset = CustomUser.objects.filter(business_group=business_group)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['employee'].queryset = self.instance.business_group.city_set