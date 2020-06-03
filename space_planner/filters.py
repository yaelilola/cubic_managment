import django_filters
from custom_user.models import BusinessGroup
from django_filters.widgets import RangeWidget


class PositionFilter(django_filters.FilterSet):
    business_group = django_filters.ModelMultipleChoiceFilter(queryset=BusinessGroup.objects.filter(admin_group=False))


class RequestsFilter(django_filters.FilterSet):
    business_group = django_filters.ModelChoiceFilter(queryset=BusinessGroup.objects.filter(admin_group=False))
