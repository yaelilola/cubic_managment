import django_tables2 as tables
from recruit.models import NewPosition
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.forms import DateInput
from CustomRequests.models import RequestToChangeCubic
from facilities.models import Space

import django_filters


class UserRequestsTable(tables.Table):
    class Meta:
        model = RequestToChangeCubic
        exclude = ['id']
        row_attrs = {
            "request_id": lambda record: record.pk
        }




