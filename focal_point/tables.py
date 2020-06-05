import django_tables2 as tables
from CustomRequests.models import RequestToChangeCubic
from assign.models import AssignUserCubic
from custom_user.models import CustomUser

import django_filters


class UserRequestsTable(tables.Table):
    class Meta:
        model = RequestToChangeCubic
        exclude = ['id']
        row_attrs = {
            "request_id": lambda record: record.pk
        }


class AssignmentsFilter(django_filters.FilterSet):
    def __init__(self, *args, users_queryset,cubics_queryset, **kwargs):
        super(AssignmentsFilter, self).__init__(*args, **kwargs)
        self.filters['assigned_user'].queryset = users_queryset
        self.filters['cubic'].queryset = cubics_queryset

    class Meta:
        model = AssignUserCubic
        fields = ['assigned_user', 'cubic']


class AssignmentsTable(tables.Table):
    class Meta:
        model = AssignUserCubic
        exclude = ['id']
        filterset_class = AssignmentsFilter
        row_attrs = {
            "user_id": lambda record: record.assigned_user.pk
        }




