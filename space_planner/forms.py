from django import forms
from custom_user.models import CustomUser, BusinessGroup

from dal import autocomplete


class ChooseFocalPointForm(forms.Form):
    business_group = forms.ModelChoiceField(queryset=BusinessGroup.objects.filter(admin_group=False))
    employee = forms.ModelChoiceField(queryset=CustomUser.objects.filter(admin=False),widget=autocomplete.ModelSelect2(url='custom_user:customuser-autocomplete',
                                                                   attrs={'data-placeholder': 'Type the user name ...','data-html': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_group'].queryset = BusinessGroup.objects.filter(admin_group=False)
        self.fields['employee'].queryset = CustomUser.objects
        if 'business_group' in self.data:
            try:
                business_group = int(self.data.get('business_group'))
                self.fields['employee'].queryset = CustomUser.objects.filter(business_group=business_group)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['business_group'].queryset = BusinessGroup.objects.filter(admin_group=False)
            self.fields['employee'].queryset = CustomUser.objects.filter(admin=False)

