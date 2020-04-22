from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import FocalPointRequest
from CustomRequests.forms import FocalPointRequestSpacePlannerForm
from assign.forms import AssignSpacesToBusinessGroupsForm
from facilities.models import Cubic, Space, Floor, Campus, Building
from custom_user.models import CustomUser, BusinessGroup
from .forms import ChooseFocalPointForm
from cubic_managment.decorators import user_is_space_planner
from assign.models import AssignUserCubic
from .tables import CampusTable, BuildingTable, FloorTable
from django_tables2 import RequestConfig

#space planner actions
@user_is_space_planner
def simulations(request):
    pass

@user_is_space_planner
def get_alerts(request):
    pass

@user_is_space_planner
def assign_space(request):
    #TODO: add logic
    if request.method == 'GET':
        return render(request, 'space_planner/assignspace.html', {'form': AssignSpacesToBusinessGroupsForm()})
    else:
        try:
            form = AssignSpacesToBusinessGroupsForm(data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    business_group = form.cleaned_data.get("business_group")
                    spaces = form.cleaned_data.get("spaces")
                    for space in spaces:
                        cubics = Cubic.objects.filter(space=space)
                        for cubic in cubics:
                            cubic.set_business_group(business_group)
                            cubic.save()
            return redirect('homepage')
        except ValueError:
            return render(request, 'space_planner/assignspace.html',
                          {'error': 'Bad info', 'form': AssignSpacesToBusinessGroupsForm()})


def get_floor_utilization(floor):
    spaces = Space.objects.filter(floor=floor)
    total_space = 0
    occupied_space = 0
    for space in spaces:
        cubics = Cubic.objects.filter(space=space)
        for cubic in cubics:
            if cubic.type == 'private':
                total_space += 1
                if len(AssignUserCubic.objects.filter(cubic=cubic)) > 0:
                    occupied_space += 1
            if cubic.type == 'shared':
                total_space += 2
                if len(AssignUserCubic.objects.filter(cubic=cubic)) == 1:
                    occupied_space += 1
                if len(AssignUserCubic.objects.filter(cubic=cubic)) == 2:
                    occupied_space += 2
    return total_space, occupied_space


def get_building_utilization(building):
    floors = Floor.objects.filter(building=building)
    total_space = 0
    occupied_space = 0
    for floor in floors:
        floor_total_space, floor_occupied_space = get_floor_utilization(floor)
        total_space += floor_total_space
        occupied_space += floor_occupied_space
    return total_space, occupied_space

def get_data_for_statistics():
    campuses = Campus.objects.all()
    data = []
    for campus in campuses:
        buildings = Building.objects.filter(campus=campus)
        for building in buildings:
            floors = Floor.objects.filter(building=building)
            for floor in floors:
                total_floor_space, floor_occupied_space = get_floor_utilization(floor)
                floor_info = {'Campus': campus, 'Building': building, 'Floor': floor,
                              'Total_Space': total_floor_space, 'Occupied': floor_occupied_space,
                              'Utilization': float((floor_occupied_space * 100)) / total_floor_space}
                data.append(floor_info)
    return data

def get_campus_utilization(campus):
    building = Building.objects.filter(campus=campus)
    total_space = 0
    occupied_space = 0
    for building in building:
        building_total_space, building_occupied_space = get_building_utilization(building)
        total_space += building_total_space
        occupied_space += building_occupied_space
    return total_space, occupied_space

def get_campus_statistics():
    campuses = Campus.objects.all()
    data = []
    for campus in campuses:
        campus_space, campus_utilization = get_campus_utilization(campus)
        campus_info = {'Campus': campus,
                      'Capacity': campus_space, 'Office_EEs': campus_utilization,
                      'Utilization': float((campus_utilization * 100)) / campus_space}
        data.append(campus_info)
    return data

def get_building_statistics(campus):
    buildings = Building.objects.filter(campus=campus)
    data = []
    for building in buildings:
        building_space, building_utilization = get_building_utilization(building)
        building_info = {'Building': building, 'Campus': campus,
                      'Capacity': building_space, 'Office_EEs': building_utilization,
                      'Utilization': float((building_utilization * 100)) / building_space}
        data.append(building_info)
    return data


def get_floor_statistics(building):
    floors = Floor.objects.filter(building=building)
    data = []
    for floor in floors:
        floor_space, floor_utilization = get_floor_utilization(floor)
        floor_info = {'Floor': floor, 'Building': '', 'Campus': '',
                      'Capacity': floor_space, 'Office_EEs': floor_utilization,
                      'Utilization': float((floor_utilization * 100)) / floor_space}
        data.append(floor_info)
    return data


def get_building_table(request, campus_id):
    data = get_building_statistics(campus_id)
    table = BuildingTable(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/building_statistics.html', {'table': table, 'campus_id': campus_id})


def get_floor_table(request, campus_id, building_id):
    data = get_floor_statistics(building_id)
    building = get_object_or_404(Building, id=building_id)
    campus = building.campus
    path = str(campus) + "/" + str(building_id)
    table = FloorTable(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/floor_statistics.html', {'table': table, 'campus_id': campus_id,
                                                                   'building_id': building_id})


@user_is_space_planner
def get_statistics(request):
    data = get_campus_statistics()
    table = CampusTable(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/campus_statistics.html', {'table': table})


@user_is_space_planner
def display_requests(request):
    requests = FocalPointRequest.objects.all()
    return render(request, 'space_planner/requests.html', {'requests': requests})


@user_is_space_planner
def display_request(request, request_id):
    focal_point_request = get_object_or_404(FocalPointRequest, pk=request_id)
    if request.method == 'GET':
        form = FocalPointRequestSpacePlannerForm(instance=focal_point_request)
        return render(request, 'space_planner/viewrequest.html', {'request': focal_point_request, 'form': form})
    else:
        try:
            form = FocalPointRequestSpacePlannerForm(request.POST, instance=focal_point_request)
            form.save()
            return redirect('space_planner:requests')
        except ValueError:
            return render(request, 'space_planner/viewrequest.html',
                          {'request': focal_point_request, 'error': 'Bad info', 'form': form})

@user_is_space_planner
def assign_focal_point(request):
    if request.method == 'GET':
        return render(request, 'space_planner/assign_focal_point.html', {'form': ChooseFocalPointForm()})
    else:
        # try:
            if request.POST:
                chosen_business_group_query_set = BusinessGroup.objects.filter(id=request.POST.get('business_group'),
                                                                               admin_group=False)
                chosen_employee_query_set = CustomUser.objects.filter(email=request.POST.get('employee'))
                chosen_employee = chosen_employee_query_set[0]  # should be only one
                old_focal_point_exists = len(CustomUser.objects.filter(business_group=
                                                                       chosen_business_group_query_set[0],
                                                                       focal_point=True)) > 0
                if old_focal_point_exists:
                    old_focal_point = CustomUser.objects.filter(business_group=chosen_business_group_query_set[0],
                                                                focal_point=True)[0]
                    old_focal_point.focal_point = False
                    old_focal_point.save()
                chosen_employee.focal_point = True
                chosen_employee.save()
                return redirect('homepage')
        # except ValueError or IndexError:
        #     return render(request, 'space_planner/assign_focal_point.html',
        #                   {'form': ChooseFocalPointForm(), 'error': 'Bad info'})


@user_is_space_planner
def load_employees(request):
    chosen_business_group = request.GET.get('business_group')
    employees = CustomUser.objects.filter(business_group=chosen_business_group)
    return render(request, 'space_planner/employees_dropdown_list_options.html', {'employees': employees})



