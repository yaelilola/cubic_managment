from django.contrib.auth.forms import UserCreationForm
from custom_user.models import CustomUser,BusinessGroup
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# class CustomUserSignUpForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('employee_number', 'password', 'type', 'start_date', 'end_date', 'percentage', 'group')
#


class CustomUserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CustomUserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['business_group'].queryset = BusinessGroup.objects.filter(admin_group=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'employee_number', 'focal_point', 'space_planner', 'percentage', 'business_group',
                  'start_date', 'end_date')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email','employee_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class SearchUserCubicForm(forms.Form):
    user = forms.ModelChoiceField(CustomUser.objects.all())

    def __init__(self,users_query_set, *args, **kwargs):
        super(SearchUserCubicForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = users_query_set





