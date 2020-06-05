from django.shortcuts import render, get_object_or_404
from facilities.models import Campus, Building, Floor, Space, Cubic, Lab
from cubic_managment.decorators import user_is_space_planner
from space_planner.tables import CubicsTable, CubicsFilter, LabsTable, LabsFilter
from django_tables2 import RequestConfig
from custom_user.models import BusinessGroup
from itertools import chain

# Create your views here.

@user_is_space_planner
def display_campuses(request):
    campuses = Campus.objects.all()
    return render(request, 'facilities/campuses.html', {'items': campuses})

@user_is_space_planner
def display_campus(request, campus_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    buildings = Building.objects.filter(campus=wanted_campus)
    return render(request, 'facilities/buildings.html', {'items': buildings, 'campus_id': campus_id})

@user_is_space_planner
def display_building(request, campus_id, building_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    floors = Floor.objects.filter(building=wanted_building)
    return render(request, 'facilities/floors.html', {'items': floors, 'campus_id': campus_id,
                                                      'building_id': building_id})

@user_is_space_planner
def display_floor(request, campus_id, building_id, floor_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, id=floor_id)
    spaces = Space.objects.filter(floor=wanted_floor)
    return render(request, 'facilities/spaces.html', {'items': spaces, 'campus_id': campus_id,
                                                      'building_id': building_id, 'floor_id': floor_id})

@user_is_space_planner
def display_space(request, campus_id, building_id, floor_id, space_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, id=floor_id)
    wanted_space = get_object_or_404(Space, floor=wanted_floor, id=space_id)
    cubics = Cubic.objects.filter(space=wanted_space)
    labs = Lab.objects.filter(space=wanted_space)
    items = chain(cubics, labs)
    return render(request, 'facilities/cubics.html', {'items': items, 'campus_id': campus_id,
                                                      'building_id': building_id,
                                                      'floor_id': floor_id, 'space_id': space_id})

@user_is_space_planner
def display_cubic(request, campus_id, building_id, floor_id, space_id, cubic_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, id=floor_id)
    wanted_space = get_object_or_404(Space, floor=wanted_floor, id=space_id)
    cubic = get_object_or_404(Cubic, space=wanted_space, id=cubic_id)
    return render(request, 'facilities/cubic.html', {'campus_id': campus_id, 'building_id': building_id,
                                                     'floor_id': floor_id, 'space_id': space_id, 'cubic': cubic})


@user_is_space_planner
def display_all_cubics(request):
    all_cubics = Cubic.objects.all()
    business_groups = BusinessGroup.objects.filter(admin_group=False)
    spaces = Space.objects.all()
    cubic_filter = CubicsFilter(request.GET, queryset=all_cubics, business_groups_queryset=business_groups,
                                spaces_queryset=spaces)
    table = CubicsTable(cubic_filter.qs, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 10, "page": 1}).configure(table)
    return render(request, 'facilities/cubic.html', {'table': table, 'filter': cubic_filter})


@user_is_space_planner
def display_all_labs(request):
    all_labs = Lab.objects.all()
    labs_filter = LabsFilter(request.GET, queryset=all_labs)
    table = LabsTable(labs_filter.qs, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 20, "page": 1}).configure(table)
    return render(request, 'facilities/labs.html', {'table': table, 'filter': labs_filter})



