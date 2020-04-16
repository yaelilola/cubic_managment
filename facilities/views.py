from django.shortcuts import render, get_object_or_404
from facilities.models import Campus, Building, Floor, Space, Cubic
# Create your views here.


def display_campuses(request):
    campuses = Campus.objects.all()
    return render(request, 'facilities/campuses.html', {'items': campuses})


def display_campus(request, campus_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    buildings = Building.objects.filter(campus=wanted_campus)
    return render(request, 'facilities/buildings.html', {'items': buildings, 'campus_id': campus_id})


def display_building(request,campus_id,building_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building,campus=wanted_campus,id=building_id)
    floors = Floor.objects.filter(building=wanted_building)
    return render(request, 'facilities/floors.html', {'items': floors,'campus_id':campus_id,'building_id':building_id})


def display_floor(request,campus_id,building_id,floor_num):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, floor_num=int(floor_num))
    spaces = Space.objects.filter(floor=wanted_floor)
    return render(request, 'facilities/spaces.html', {'items': spaces})


def display_space(request,campus_id,building_id,floor_num,space_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, floor_num=int(floor_num))
    wanted_space = get_object_or_404(Space,floor=wanted_floor,id=space_id)
    cubics = Cubic.objects.filter(space=wanted_space)
    return render(request, 'facilities/cubics.html', {'items': cubics})


def display_cubic(request,campus_id,building_id,floor_num,space_id,cubic_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    wanted_building = get_object_or_404(Building, campus=wanted_campus, id=building_id)
    wanted_floor = get_object_or_404(Floor, building=wanted_building, floor_num=int(floor_num))
    wanted_space = get_object_or_404(Space, floor=wanted_floor, id=space_id)
    cubic = get_object_or_404(Cubic,space=wanted_space,id=cubic_id)
    return render(request, 'facilities/cubic.html', {'cubic': cubic,'campus':campus_id,'building':building_id,'floor':floor_num,'space':space_id})


