import django_tables2 as tables

class CampusTable(tables.Table):
    Campus = tables.Column(orderable=True,
                           linkify={"viewname": "space_planner:get_building_table", "args": [tables.A("Campus__pk")]})
    Total_Space = tables.Column(orderable=True)
    Occupied = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class BuildingTable(tables.Table):
    Building = tables.Column(orderable=True,
                             linkify={"viewname": "space_planner:get_floor_table", "args": [tables.A("Building__pk")]})
    Total_Space = tables.Column(orderable=True)
    Occupied = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class FloorTable(tables.Table):
    Floor = tables.Column(orderable=True)
    Total_Space = tables.Column(orderable=True)
    Occupied = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)


class NameTable(tables.Table):
    Campus = tables.Column(orderable=True)
    Building = tables.Column(orderable=True)
    Floor = tables.Column(orderable=True)
    Total_Space = tables.Column(orderable=True)
    Occupied = tables.Column(orderable=True)
    Utilization = tables.Column(orderable=True)

