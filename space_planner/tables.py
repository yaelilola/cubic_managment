import django_tables2 as tables
from recruit.models import NewPosition
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.forms import DateInput
import django_filters

class CampusTable(tables.Table):
    Campus = tables.Column(orderable=True,
                           linkify={"viewname": "space_planner:get_building_table", "args": [tables.A("Campus__pk")]})
    Capacity = tables.Column(orderable=True)
    Office_EEs = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class BuildingTable(tables.Table):
    Campus = tables.Column(visible=False)
    Building = tables.Column(orderable=True,
                             linkify={"viewname": "space_planner:get_floor_table",
                                      "args": [tables.A('Campus'), tables.A('Building')]})

    Capacity = tables.Column(orderable=True)
    Office_EEs = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class FloorTable(tables.Table):
    Floor = tables.Column(orderable=True)
    Capacity = tables.Column(orderable=True)
    Office_EEs = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class NameTable(tables.Table):
    Campus = tables.Column(orderable=True)
    Building = tables.Column(orderable=True)
    Floor = tables.Column(orderable=True)
    Total_Space = tables.Column(orderable=True)
    Occupied = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)

class PositionFilter(django_filters.FilterSet):
    class Meta:
        model = NewPosition
        fields = ['business_group', 'creation_date']


class NewPositionTable(tables.Table):
    class Meta:
        model = NewPosition
        exclude = ['id']
        filterset_class = PositionFilter


