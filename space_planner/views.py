from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import FocalPointRequest
from CustomRequests.forms import FocalPointRequestSpacePlannerForm
from assign.forms import AssignSpacesToBusinessGroupsForm
from facilities.models import Cubic, Space, Floor, Campus, Building, Lab
from custom_user.models import CustomUser, BusinessGroup
from .forms import ChooseFocalPointForm
from cubic_managment.decorators import user_is_space_planner
from assign.models import AssignUserCubic
from .tables import CampusTable, CampusTable_no_mean, BuildingTable, BuildingTable_no_mean, FloorTable, \
    FloorTable_no_mean, NewPositionTable, FocalPointRequestsTable, SpacesTable, AlertsTable
from django_tables2 import RequestConfig
from recruit.models import NewPosition
from .filters import PositionFilter, RequestsFilter
from django.core.mail import send_mail
from datetime import date
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
import os

#space planner actions
@user_is_space_planner
def simulations(request):
    pass


def two_months_ago():
    today = date.today()
    return today - relativedelta(months=2)


def get_amount_of_positions(bg, percentage):
    business_group_new_positions = NewPosition.objects.filter(business_group=bg)
    if percentage == 'full_time':
        if len(business_group_new_positions) > 0:
            return business_group_new_positions[0].college_graduate_internal_and_external + \
                   business_group_new_positions[0].experienced_internal_and_external +\
                   business_group_new_positions[0].intel_contract_employee_internal_and_external +\
                   business_group_new_positions[0].technical_graduate_internal_and_external + \
                   business_group_new_positions[0].college_graduate_internal_only + \
                   business_group_new_positions[0].experienced_internal_only + \
                   business_group_new_positions[0].intel_contract_employee_internal_only + \
                   business_group_new_positions[0].technical_graduate_internal_only
        else:
            return 0
    #looking for part time positions
    else:
        if len(business_group_new_positions) > 0:
            return business_group_new_positions[0].student_intern_internal_and_external + \
                   business_group_new_positions[0].student_intern_internal_only
        else:
            return 0


@user_is_space_planner
def get_alerts(request):
    if request.method == 'GET':
        data = []
        wanted_business_groups = BusinessGroup.objects.filter(admin_group=False)
        for bg in wanted_business_groups:
            bg_free_shared_cubics_amount = get_available_cubics_as_list(bg, 1, 'shared')
            bg_free_private_cubics_amount = get_available_cubics_as_list(bg)
            # searches all new position
            bg_full_time_new_positions_amount = get_amount_of_positions(bg, 'full_time')
            bg_part_time_new_positions_amount = get_amount_of_positions(bg, 'part_time')
            bg_info = {'Business_Group': str(bg), 'Full_Time_New_Positions_Amount': bg_full_time_new_positions_amount,
                       'Part_Time_New_Positions_Amount': bg_part_time_new_positions_amount,
                       'Available_Private_Cubics': bg_free_private_cubics_amount,
                       'Available_Shared_Cubics': bg_free_shared_cubics_amount}
            if bg_free_private_cubics_amount == 0:
                bg_info.update({'Full_Time_Cubics_Expected_Utilization': 200})
            else:
                bg_info.update(
                    {'Full_Time_Cubics_Expected_Utilization':
                     bg_full_time_new_positions_amount*100 / bg_free_private_cubics_amount})
            if bg_free_shared_cubics_amount == 0:
                bg_info.update({'Part_Time_Cubics_Expected_Utilization': 200})
            else:
                bg_info.update({'Part_Time_Cubics_Expected_Utilization':
                                    bg_part_time_new_positions_amount * 100 / bg_free_shared_cubics_amount})
            data.append(bg_info)
        table = AlertsTable(data, template_name="django_tables2/bootstrap.html")
        RequestConfig(request, paginate={"per_page": 30, "page": 1}).configure(table)
        return render(request, 'space_planner/alerts.html', {'table': table})

def get_business_group_requests(request):
    wanted_business_groups = BusinessGroup.objects.filter(admin_group=False)
    requests_list = FocalPointRequest.objects.filter(business_group__in=wanted_business_groups)
    requests_filter = RequestsFilter(request.GET, queryset=requests_list)
    # return render(request, 'space_planner/new_positions.html', {'filter': positions_filter})
    table = FocalPointRequestsTable(requests_filter.qs, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 10, "page": 1}).configure(table)
    return table, requests_filter

def find_groups_in_floor(floor):
    groups = []
    groups_str = ""
    spaces = Space.objects.filter(floor=floor)
    for space in spaces:
        cubics = Cubic.objects.filter(space=space)
        for cubic in cubics:
            if cubic.business_group:
                groups.append(str(cubic.business_group))
    groups_no_dups = list(set(groups))
    if len(groups_no_dups) > 0:
        for i in range(len(groups_no_dups)-1):
            groups_str += (groups_no_dups[i] + ",")
        groups_str += groups_no_dups[len(groups_no_dups)-1]
    return groups_str


def get_spaces_with_room(request, floor):
    spaces = Space.objects.filter(floor=floor)
    data = []
    for space in spaces:
        total_space, private_free_space, shared_free_space = get_amount_available_cubics_in_space(space)
        if private_free_space > 0 or shared_free_space > 0:
            floor = space.floor
            groups_in_floor = find_groups_in_floor(floor)
            building = floor.building
            campus = building.campus
            near_low_density_lab = False
            low_density_labs = Lab.objects.filter(type="Low Density Lab", floor=floor)
            if low_density_labs.exists():
                near_low_density_lab = True
            near_high_density_lab = False
            low_density_labs = Lab.objects.filter(type="High Density Lab", floor=floor)
            if low_density_labs.exists():
                near_high_density_lab = True
            space_info = {'Campus': campus, 'Building': building, 'Floor': space.floor, 'Id': space.id,
                            'Free_Private': private_free_space, 'Free_Shared': shared_free_space,
                          'Near_Low_Density_Lab': near_low_density_lab, 'Near_High_Density_Lab': near_high_density_lab,
                          'Groups_Nearby': groups_in_floor}
            data.append(space_info)
    table = SpacesTable(data, template_name="django_tables2/bootstrap.html")
    # RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return table


@user_is_space_planner
def assign_space(request):
    business_groups = BusinessGroup.objects.filter(admin_group=False)
    data = Space.objects.none()
    spaces_table = SpacesTable(data, template_name="django_tables2/bootstrap.html")
    # spaces_table = get_spaces_with_room(request)
    campuses = Campus.objects.all()
    if request.method == 'GET':
        requests_table, requests_filter = get_business_group_requests(request)
        return render(request, 'space_planner/assignspace.html',
                      {'business_groups': business_groups, 'campuses': campuses, 'table': spaces_table})
    else:
        try:
            if request.POST:
                business_group_id = request.POST.get("chosen_business_group")
                business_group = BusinessGroup.objects.get(id=business_group_id)
                spaces_ids = request.POST.getlist("selection")
                if not spaces_ids:
                    return render(request, 'space_planner/assignspace.html',
                                  {'error': 'must choose a space','campuses': campuses, 'table': spaces_table,
                                   'business_groups': business_groups})
                else:
                    spaces = Space.objects.filter(id__in=spaces_ids)
                    for space in spaces:
                        cubics = Cubic.objects.filter(space=space)
                        for cubic in cubics:
                            #checking if the cubic is assigned to a group
                            if cubic.business_group is None:
                                cubic.set_business_group(business_group)
                                cubic.save()
            return redirect('homepage')
        except ValueError:
            return render(request, 'space_planner/assignspace.html',
                          {'error': 'Bad info'})



# @user_is_space_planner
# def assign_space_ajax(request):
#     print(request.POST)
#     return redirect('homepage')



@user_is_space_planner
def load_requests(request):
    chosen_business_group = request.GET.get('business_group')
    requests = FocalPointRequest.objects.filter(business_group=chosen_business_group)
    if len(requests) == 0:
        return render(request, 'space_planner/focal_point_request_info.html', {'business_group': chosen_business_group})
    else:
        table = FocalPointRequestsTable(requests, template_name="django_tables2/bootstrap.html")
        table.exclude = ('status', 'notes', 'date')
        RequestConfig(request, paginate={"per_page": 10, "page": 1}).configure(table)
        return render(request, 'space_planner/focal_point_request_info.html', {'table': table,
                                                                               'business_group': chosen_business_group})


def load_spaces(request):
    chosen_floor = request.GET.get('floor')
    avail_spaces = get_spaces_with_room(request, chosen_floor)
    return render(request, 'space_planner/focal_point_request_info.html', {'table': avail_spaces})




def load_campus_buildings(request):
    chosen_campus = request.GET.get('campus')
    buildings = Building.objects.filter(campus=chosen_campus)
    return render(request, 'space_planner/buildings_dropdown_list_options.html', {'buildings': buildings})


def load_campus_buildings_floors(request):
    chosen_building = request.GET.get('building')
    floors = Floor.objects.filter(building=chosen_building)
    return render(request, 'space_planner/floors_dropdown_list_options.html', {'floors': floors})

def get_amount_available_cubics_in_space(space):
    total_space = 0
    private_free_space = 0
    shared_free_space = 0
    private_cubics = Cubic.objects.filter(space=space, type='private')
    total_space += len(private_cubics)
    shared_cubics = Cubic.objects.filter(space=space, type='shared')
    for cubic in shared_cubics:
        total_space += cubic.capacity
    free_private_cubics = private_cubics.filter(business_group__isnull=True)
    private_free_space += len(free_private_cubics)
    free_shared_cubics = shared_cubics.filter(business_group__isnull=True)
    for cubic in free_shared_cubics:
        shared_free_space += cubic.capacity
    return total_space, private_free_space, shared_free_space


def get_space_utilization(space, business_group=None):
    total_space = 0
    occupied_space = 0
    private_space = 0
    shared_space = 0
    if business_group is None: #space planner purpose
        cubics = Cubic.objects.filter(space=space)
    else:
        cubics = Cubic.objects.filter(space=space, business_group=business_group)
    for cubic in cubics:
        if cubic.type == 'private':
            total_space += 1
            if len(AssignUserCubic.objects.filter(cubic=cubic)) > 0:
                occupied_space += 1
            else:
                private_space += 1
        if cubic.type == 'shared':
            total_space += cubic.capacity
            cubic_assignments_amount = len(AssignUserCubic.objects.filter(cubic=cubic))
            if cubic_assignments_amount < cubic.capacity:
                occupied_space += cubic_assignments_amount
                shared_space += (cubic.capacity-cubic_assignments_amount)
            elif cubic_assignments_amount == cubic.capacity:
                occupied_space += cubic.capacity
    return total_space, occupied_space, private_space, shared_space



def get_floor_utilization(floor,business_group=None):
    spaces = Space.objects.filter(floor=floor)
    total_space = 0
    occupied_space = 0
    for space in spaces:
        space_total_space, space_occupied_space, private_space, shared_space = get_space_utilization(space,business_group)
        total_space += space_total_space
        occupied_space += space_occupied_space
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
                              'Utilization': 200 if total_floor_space == 0 else float((floor_occupied_space * 100)) / total_floor_space}
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
                      'Utilization': 200 if campus_space == 0 else float((campus_utilization * 100)) / campus_space}
        data.append(campus_info)
    return data

def get_building_statistics(campus):
    buildings = Building.objects.filter(campus=campus)
    data = []
    for building in buildings:
        building_space, building_utilization = get_building_utilization(building)
        building_info = {'Building': building, 'Campus': campus,
                      'Capacity': building_space, 'Office_EEs': building_utilization,
                      'Utilization': 200 if building_space == 0 else float((building_utilization * 100)) / building_space}
        data.append(building_info)
    return data


def get_floor_statistics(building):
    floors = Floor.objects.filter(building=building)
    data = []
    for floor in floors:
        floor_space, floor_utilization = get_floor_utilization(floor)
        if floor_space == 0:
            floor_info = {'Floor': floor, 'Building': '', 'Campus': '',
                          'Capacity': floor_space, 'Office_EEs': floor_utilization,
                          'Utilization': 200}
        else:
            floor_info = {'Floor': floor, 'Building': '', 'Campus': '',
                          'Capacity': floor_space, 'Office_EEs': floor_utilization,
                          'Utilization': float((floor_utilization * 100)) / floor_space}
        data.append(floor_info)
    return data

@user_is_space_planner
def get_building_table(request, campus_id):
    data = get_building_statistics(campus_id)
    if len(data)>0:
        table = BuildingTable(data, template_name="django_tables2/bootstrap.html")
    else:
        table = BuildingTable_no_mean(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/building_statistics.html', {'table': table, 'campus_id': campus_id})

@user_is_space_planner
def get_floor_table(request, campus_id, building_id):
    data = get_floor_statistics(building_id)
    building = get_object_or_404(Building, id=building_id)
    campus = building.campus
    path = str(campus) + "/" + str(building_id)
    if len(data)>0:
        table = FloorTable(data, template_name="django_tables2/bootstrap.html")
    else:
        table = FloorTable_no_mean(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/floor_statistics.html', {'table': table, 'campus_id': campus_id,
                                                                   'building_id': building_id})


@user_is_space_planner
def get_statistics(request):
    data = get_campus_statistics()
    if len(data)>0:
        table = CampusTable(data, template_name="django_tables2/bootstrap.html")
    else:
        table = CampusTable_no_mean(data, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/campus_statistics.html', {'table': table})


@user_is_space_planner
def display_new_positions(request):
    # table = NewPositionTable(NewPosition.objects.all())
    # RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    # return render(request, 'space_planner/new_positions.html', {'table': table})
    wanted_business_groups = BusinessGroup.objects.filter(admin_group=False)
    positions_list = NewPosition.objects.filter(business_group__in=wanted_business_groups)
    positions_filter = PositionFilter(request.GET, queryset=positions_list)
    #return render(request, 'space_planner/new_positions.html', {'filter': positions_filter})
    table = NewPositionTable(positions_filter.qs, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'space_planner/new_positions.html', {'table': table, 'filter': positions_filter})

@user_is_space_planner
def display_requests(request):
    requests = FocalPointRequest.objects.all()
    table = FocalPointRequestsTable(requests, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 10, "page": 1}).configure(table)
    return render(request, 'space_planner/requests.html', {'table': table})


def send_change_status_notification(request, request_content):
    sender_mail = os.environ['EMAIL_HOST_USER'] #TODO - change to real mail
    space_planner = request.user.email
    request_business_group = (request_content['business_group'])
    request_focal_point = get_object_or_404(CustomUser, focal_point=True, business_group=request_business_group)
    receiver_mail=request_focal_point.email
    subject = "Request from space planner status update"
    content = "{space_planner} changed your request status to '{status}'".format(space_planner=space_planner, status=request_content['status'])
    send_mail(subject, content,
              sender_mail,
              [receiver_mail])

@user_is_space_planner
def display_request(request, request_id):
    focal_point_request = get_object_or_404(FocalPointRequest, pk=request_id)
    if request.method == 'GET':
        form = FocalPointRequestSpacePlannerForm(instance=focal_point_request)
        return render(request, 'space_planner/viewrequest.html', {'request': focal_point_request, 'form': form})
    else:
        try:
            orig_request_status = focal_point_request.status
            request_post_copy = request.POST.copy()
            request_post_copy['business_group'] = focal_point_request.business_group
            request_post_copy['part_time_employees_amount'] = focal_point_request.part_time_employees_amount
            request_post_copy['full_time_employees_amount'] = focal_point_request.full_time_employees_amount
            request_post_copy['business_group_near_by'] = focal_point_request.business_group_near_by
            request_post_copy['near_low_density_lab'] = focal_point_request.near_low_density_lab
            request_post_copy['near_high_density_lab'] = focal_point_request.near_high_density_lab
            request_post_copy['date'] = focal_point_request.date
            request_post_copy['destination_date'] = focal_point_request.destination_date
            form = FocalPointRequestSpacePlannerForm(request_post_copy, instance=focal_point_request)
            form.save()
            if request_post_copy['status'] != orig_request_status:
                send_change_status_notification(request, request_post_copy)
            return redirect('space_planner:requests')
        except ValueError:
            return render(request, 'space_planner/viewrequest.html',
                          {'request': focal_point_request, 'error': 'Bad info', 'form': form})


def send_no_longer_focal_point_notification(space_planner_email, previous_focal_point_email):
    sender_mail = os.environ['EMAIL_HOST_USER']  # TODO - change to real mail
    receiver_mail = previous_focal_point_email
    subject = "You are no longer a focal point."
    content = "{space_planner} assigned a new focal point for your group.".format(space_planner=space_planner_email)
    send_mail(subject, content,
              sender_mail,
              [receiver_mail])


def send_new_focal_point_notification(space_planner_email, new_focal_point_email):
    sender_mail = os.environ['EMAIL_HOST_USER']  # TODO - change to real mail
    receiver_mail = new_focal_point_email
    subject = "You are the new focal point for your group."
    content = "{space_planner} assigned you as the new group focal point.".format(space_planner=space_planner_email)
    send_mail(subject, content,
              sender_mail,
              [receiver_mail])


@user_is_space_planner
def assign_focal_point(request):
    if request.method == 'GET':
        return render(request, 'space_planner/assign_focal_point.html', {'form': ChooseFocalPointForm()})
    else:
        try:
            if request.POST:
                chosen_business_group_query_set = BusinessGroup.objects.filter(id=request.POST.get('business_group'),
                                                                               admin_group=False)
                chosen_employee_query_set = CustomUser.objects.filter(employee_number=request.POST.get('employee'))
                if len(chosen_business_group_query_set) == 0 or len(chosen_employee_query_set) == 0: #cant submit form with at least one empty field
                    return render(request, 'space_planner/assign_focal_point.html', {'form': ChooseFocalPointForm(),
                                                                                     'error': 'please fill all forms'})
                else:
                    chosen_employee = chosen_employee_query_set[0]  # should be only one
                    old_focal_point_exists = len(CustomUser.objects.filter(business_group=
                                                                           chosen_business_group_query_set[0],
                                                                           focal_point=True)) > 0
                    if old_focal_point_exists:
                        old_focal_point = CustomUser.objects.filter(business_group=chosen_business_group_query_set[0],
                                                                    focal_point=True)[0]
                        old_focal_point.focal_point = False
                        old_focal_point.save()
                        send_no_longer_focal_point_notification(request.user.email, old_focal_point.email)
                    chosen_employee.focal_point = True
                    chosen_employee.save()
                    send_new_focal_point_notification(request.user.email, chosen_employee.email)
                    return redirect('homepage')
        except ValueError or IndexError:
            return render(request, 'space_planner/assign_focal_point.html',
                          {'form': ChooseFocalPointForm(), 'error': 'Bad info'})


@user_is_space_planner
def load_employees(request):
    chosen_business_group = request.GET.get('business_group')
    employees = CustomUser.objects.filter(business_group=chosen_business_group)
    return render(request, 'space_planner/employees_dropdown_list_options.html', {'employees': employees})



def cubic_avail_places(cubic):
    assignments_amount = len(AssignUserCubic.objects.filter(cubic=cubic))
    # if its non positive its not available
    return cubic.capacity-assignments_amount


def get_available_cubics_as_list(business_group, person_amount=1, cubic_type='private'):
    cubics_queryset_aux = Cubic.objects.filter(business_group=business_group, type=cubic_type)
    # avail_cubics = []
    avail_cubics = 0
    for cubic in cubics_queryset_aux:
        cubic_left_capacity = cubic_avail_places(cubic)
        if cubic_left_capacity >= person_amount:
            avail_cubics += cubic_left_capacity
    return avail_cubics