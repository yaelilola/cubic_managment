import django_tables2 as tables
from recruit.models import NewPosition
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.forms import DateInput
from CustomRequests.models import FocalPointRequest
from facilities.models import Space
from statistics import mean
from facilities.models import Cubic

import django_filters

class ColumnWithName(tables.Column):
    @property
    def header(self):
        return self.verbose_name

class CampusTable(tables.Table):
    Campus = tables.Column(orderable=True,
                           linkify={"viewname": "space_planner:get_building_table", "args": [tables.A("Campus__pk")]},
                           empty_values=(), footer='Total:')
    Capacity = tables.Column(orderable=True, footer=lambda table: sum(x["Capacity"] for x in table.data))
    Office_EEs = tables.Column(orderable=True, footer=lambda table: sum(x["Office_EEs"] for x in table.data))
    Utilization = ColumnWithName(verbose_name="Utilization(%)", orderable=True, attrs={"td": {"class": "utilization"}},
                                 footer=lambda table: mean(x["Utilization"] for x in table.data))
    #Utilization = tables.Column(orderable=True, attrs={"td": {"class": "utilization"}})


class BuildingTable(tables.Table):
    Campus = tables.Column(visible=False)
    Building = tables.Column(orderable=True, empty_values=(), footer='Total:',
                             linkify={"viewname": "space_planner:get_floor_table",
                                      "args": [tables.A('Campus'), tables.A('Building')]})

    Capacity = tables.Column(orderable=True, footer=lambda table: sum(x["Capacity"] for x in table.data))
    Office_EEs = tables.Column(orderable=True, footer=lambda table: sum(x["Office_EEs"] for x in table.data))
    Utilization = ColumnWithName(verbose_name="Utilization(%)", orderable=True, attrs={"td": {"class": "utilization"}},
                                 footer=lambda table: mean(x["Utilization"] for x in table.data))


class FloorTable(tables.Table):
    Floor = tables.Column(orderable=True, empty_values=(), footer='Total:')
    Capacity = tables.Column(orderable=True, footer=lambda table: sum(x["Capacity"] for x in table.data))
    Office_EEs = tables.Column(orderable=True, footer=lambda table: sum(x["Office_EEs"] for x in table.data))
    Utilization = ColumnWithName(verbose_name="Utilization(%)", orderable=True, attrs={"td": {"class": "utilization"}},
                                 footer=lambda table: mean(x["Utilization"] for x in table.data))


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


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = FocalPointRequest
        fields = ['business_group']


class FocalPointRequestsTable(tables.Table):
    class Meta:
        model = FocalPointRequest
        exclude = ['id']
        filterset_class = RequestFilter
        row_attrs = {
            "request_id": lambda record: record.pk
        }



class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name

class SpacesTable(tables.Table):
    #template = '<input type="checkbox" name="Chosen"/>'
    #Chosen = tables.TemplateColumn(template)
    #selection = tables.CheckBoxColumn(accessor='Id')
    selection = CheckBoxColumnWithName(verbose_name="Chosen", accessor="Id", empty_values=(), footer='Total:')
    Campus = tables.Column(orderable=True)
    Building = tables.Column(orderable=True)
    Floor = tables.Column(orderable=True)
    Id = tables.Column(orderable=True)
    Free_Private = tables.Column(orderable=True, attrs={'cell': {'class': 'free_private'}})
    Free_Shared = tables.Column(orderable=True, attrs={'cell': {'class': 'free_shared'}})
    Near_Low_Density_Lab = tables.BooleanColumn(orderable=True, attrs={'cell': {'class': 'low_density'}})
    Near_High_Density_Lab = tables.BooleanColumn(orderable=True, attrs={'cell': {'class': 'high_density'}})
    Groups_Nearby = tables.Column(attrs={'cell': {'class': 'business_groups'}})


class CubicsFilter(django_filters.FilterSet):
    area__gte = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    area__lte = django_filters.NumberFilter(field_name='area', lookup_expr='lte')
    def __init__(self, *args, business_groups_queryset, spaces_queryset, **kwargs):
        super(CubicsFilter, self).__init__(*args, **kwargs)
        self.filters['business_group'].queryset = business_groups_queryset
        self.filters['space'].queryset = spaces_queryset

    class Meta:
        model = Cubic
        fields = ['id', 'type', 'space', 'business_group', 'area', 'floor', 'building', 'campus']

class CubicsTable(tables.Table):
    area = tables.Column(footer=lambda table: sum(x.area for x in table.data))
    class Meta:
        model = Cubic
        filterset_class = CubicsFilter
        fields = ['id', 'type', 'space', 'business_group', 'floor', 'building', 'campus']

class LabsFilter(django_filters.FilterSet):
    area__gte = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    area__lte = django_filters.NumberFilter(field_name='area', lookup_expr='lte')
    type = django_filters.ChoiceFilter(choices=(('Low Density Lab', 'Low Density Lab'), ('High Density Lab', 'High Density Lab')))

    class Meta:
        model = Space
        fields = ['id', 'type', 'floor', 'building', 'campus', 'area']

class LabsTable(tables.Table):
    area = tables.Column(footer=lambda table: sum(x.area for x in table.data))
    class Meta:
        model = Space
        filterset_class = LabsFilter
        fields = ['id', 'type', 'floor', 'building', 'campus']









