from recruit.models import NewPosition
import django_filters
from custom_user.models import BusinessGroup
from .tables import FengyuanChenDatePickerInput
from django import forms

class PositionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    percentage = django_filters.ChoiceFilter(choices=(('full_time', 'full_time'), ('part_time', 'part_time')))
    business_group = django_filters.ModelMultipleChoiceFilter(queryset=BusinessGroup.objects.filter(admin_group=False))
    # created_after = django_filters.DateTimeFilter(input_formats=['%d/%m/%Y %H:%M'],
    #     widget=FengyuanChenDatePickerInput(), lookup_expr='date_gt')
    # created_before = django_filters.DateTimeFilter(input_formats=['%d/%m/%Y %H:%M'],
    #                                               widget=FengyuanChenDatePickerInput(), lookup_expr='date_lt')

    # class Meta:
    #     fields = ['name', 'percentage', 'business_group', 'creation_date']
    created_after = django_filters.DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}), name=)
    created_before = django_filters.DateFilter(widget=forms.DateInput(attrs={'class': 'datepicker'}))