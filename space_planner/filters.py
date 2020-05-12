import django_filters
from custom_user.models import BusinessGroup
from django_filters.widgets import RangeWidget


class PositionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    percentage = django_filters.ChoiceFilter(choices=(('full_time', 'full_time'), ('part_time', 'part_time')))
    business_group = django_filters.ModelMultipleChoiceFilter(queryset=BusinessGroup.objects.filter(admin_group=False))
    creation_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'dd/mm/yyyy',

                                                                                   'type': 'date'}))

class RequestsFilter(django_filters.FilterSet):
    business_group = django_filters.ModelChoiceFilter(queryset=BusinessGroup.objects.filter(admin_group=False))
