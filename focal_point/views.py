from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from CustomRequests.forms import RequestToChangeCubicFocalPointForm, FocalPointRequestForm
from assign.forms import AssignPartTimeUserCubicForm, AssignFullTimeUserCubicForm
from assign.models import AssignUserCubic
from recruit.models import NewPosition
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic, Campus, Building, Floor
from cubic_managment.decorators import user_is_focal_point, user_is_focal_point_request_author, \
    user_in_focal_point_group, request_user_in_focal_point_group
import datetime
# from django.core.mail import send_mail
from .tables import UserRequestsTable, AssignmentsTable, AssignmentsFilter
from django_tables2 import RequestConfig
from space_planner.tables import NewPositionTable
from space_planner.filters import PositionFilter

# Create your views here.
#foacl point actions

"""
View all of the assignment to focal point amde
"""
@user_is_focal_point
def view_assignments(request):
    cubics_of_business_group = Cubic.objects.filter(business_group=request.user.business_group)
    users_in_business_group = CustomUser.objects.filter(business_group=request.user.business_group)
    assignments = AssignUserCubic.objects.filter(assigned_user__in=users_in_business_group)
    assignments_filter = AssignmentsFilter(request.GET, users_queryset=users_in_business_group,
                                           cubics_queryset=cubics_of_business_group, queryset=assignments)
    table = AssignmentsTable(assignments_filter.qs, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'focal_point/assignments.html', {'table': table,'filter': assignments_filter})


def is_cubic_available(cubic, person_amount=1):
    if cubic.type == 'private':
        if len(AssignUserCubic.objects.filter(cubic=cubic)) < 1 and person_amount == 1:
            return True
        else:
            return False
    else:
    #should be shared
        if len(AssignUserCubic.objects.filter(cubic=cubic))+person_amount <= cubic.capacity:
            return True
        else:
            return False


def get_available_cubics_as_list(business_group, person_amount=1, cubic_type='private'):
    cubics_queryset_aux = Cubic.objects.filter(business_group=business_group, type=cubic_type)
    avail_cubics = []
    for cubic in cubics_queryset_aux:
        if is_cubic_available(cubic, person_amount)is True:
            avail_cubics.append(cubic)
    return avail_cubics


def get_available_cubics(business_group, person_amount=1, cubic_type='private'):
    cubics_queryset_aux = Cubic.objects.filter(business_group=business_group, type=cubic_type)
    cubics_queryset = cubics_queryset_aux
    for cubic in cubics_queryset_aux:
        if is_cubic_available(cubic, person_amount)is False:
            cubics_queryset = cubics_queryset.exclude(id=cubic.id)
    return cubics_queryset



def all_assignments_are_okay(business_group,assigned_users, cubics, cubic_type='private'):
    #TODO: assuming that private type means that cubics includes one item
    #checks if the assignment is updated to be the old one
    if cubic_type == 'private' and len(AssignUserCubic.objects.filter(cubic=cubics[0], assigned_user=assigned_users[0]))>0:
        return True
    for cubic in cubics:
        cubics_users = [assignment.assigned_user for assignment in AssignUserCubic.objects.filter(cubic=cubic)]
        users_not_in_cubic = [user for user in assigned_users if user not in cubics_users]
        available_cubics = get_available_cubics(business_group, len(users_not_in_cubic), cubic_type)
        if cubic not in available_cubics:
            return False
    return True


@user_is_focal_point
def assign_part_time(request):
    return assign(request, AssignPartTimeUserCubicForm, 'shared', 'part_time')


@user_is_focal_point
def assign_full_time(request):
    return assign(request, AssignFullTimeUserCubicForm, 'private', 'full_time')


def send_assign_notification(focal_point_email, assigned_users, cubics):
    sender_mail = "yaelAmitIndustrial@gmail.com" #TODO - change to real mail
    if len(cubics) > 1:
        subject = "You were assigned new cubics"
        content = "{focal_point} assigned you new cubics:\n".format(focal_point=focal_point_email)
        for cubic in cubics:
            space = cubic.space
            floor = space.floor
            building = floor.building
            campus = building.campus
            content += str(campus) + "\\" + str(building) + "\\" \
            + str(floor) + "\\" \
            + str(space) + "\\" \
            + str(cubic) + "\n"
    else:
        subject = "You were assigned a new cubic"
        content = "{focal_point} assigned you a new cubic:\n".format(focal_point=focal_point_email)
        space = cubics[0].space
        floor = space.floor
        building = floor.building
        campus = building.campus
        content += str(campus) + "\\" + str(building) + "\\" \
        + str(floor) + "\\" \
        + str(space) + "\\" \
        + str(cubics[0]) + "\n"
    # send_mail(subject, content, sender_mail, assigned_users)


def assign(request, form_type, cubic_type, percentage):
    #TODO - add assignment logic: should we use ajax, or check in backend?
    # focal_point = get_object_or_404(CustomUser, id=request.user.id, focal_point=True)
    business_group = request.user.business_group
    users_queryset = CustomUser.objects.filter(business_group=business_group, percentage=percentage)
    if percentage == 'full_time':
        full_not_assigned_time_users_id = [user.employee_number for user in users_queryset if len(AssignUserCubic.objects.filter(assigned_user=user)) == 0]
        users_queryset = CustomUser.objects.filter(employee_number__in=full_not_assigned_time_users_id)
    cubics_queryset = get_available_cubics(business_group, 1, cubic_type)
    if request.method == 'GET':
        return render(request, 'focal_point/assign.html',
                      {'form': form_type(users_queryset=users_queryset,user_current_cubic=[], business_group=business_group)})
    else:

        try:
            # form = form_type(users_queryset=users_queryset, cubics_queryset=cubics_queryset, data=request.POST or None)
            if request.POST:
                # print(request.POST)
                assigned_users = request.POST.getlist('users')
                # print(assigned_users)
                cubics = request.POST.getlist('cubics')
                # print(cubics)
                if cubic_type == 'private':
                    # cubics = [cubics]
                    # assigned_users = [assigned_users]
                    cubics = cubics
                    assigned_users = assigned_users
                print(assigned_users)
                assigned_users = CustomUser.objects.filter(employee_number__in=assigned_users)
                print(assigned_users)
                cubics = Cubic.objects.filter(id__in=cubics)
                print(cubics)
                #todo - complete the check if the form was empty
                if all_assignments_are_okay(business_group, assigned_users, cubics, cubic_type):
                    for user in assigned_users:
                        for cubic in cubics:
                            try:
                                assignment = AssignUserCubic(assigned_user=user, cubic=cubic)
                                print("here163")
                                assignment.save()
                                send_assign_notification(request.user.email, assigned_users, cubics)
                            except Exception as e:
                                if str(e).startswith('UNIQUE constraint failed'):
                                    pass
                else:
                    return render(request, 'focal_point/assign.html',
                                  {'form': form_type(users_queryset=users_queryset, user_current_cubic=[],
                                                     business_group=business_group),
                                   'error': 'There is not enough place in the selected cubics'})
            return redirect('focal_point:assignments')
        except ValueError:
            return render(request, 'focal_point/assign.html',
                          {'form': form_type(users_queryset=users_queryset, user_current_cubic=[], business_group=business_group), 'error': 'Bad data passed in'})



@user_is_focal_point
def edit_assignments_for_user(request, user_id, focal_point, wanted_user, current_cubics, cubic_type):
    if cubic_type == 'shared':
        form_type = AssignPartTimeUserCubicForm
    else:
        form_type = AssignFullTimeUserCubicForm
    business_group = request.user.business_group
    available_cubics = get_available_cubics(business_group, 1, cubic_type)
    available_cubics_ids = [cubic.id for cubic in available_cubics]
    # TODO: we assumed that if the user is full time, it has only one assignment
    current_cubics_ids = [cubic.id for cubic in current_cubics]
    cubics_queryset = Cubic.objects.filter(id__in=(available_cubics_ids + current_cubics_ids))
    if request.method == 'GET':
        form =form_type(users_queryset=CustomUser.objects.filter(pk=user_id),
                                            user_current_cubic=current_cubics_ids
                                           , business_group=business_group,
                                           initial={'cubics': current_cubics,'users': wanted_user})
        return render(request, 'focal_point/viewuserassignments.html', {'curr_user': wanted_user, 'form': form})
    else:
        try:
            form = form_type(users_queryset=CustomUser.objects.filter(pk=user_id), business_group=business_group,
                             user_current_cubic=current_cubics_ids,
                             data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_user = form.cleaned_data.get("users")
                    cubic = form.cleaned_data.get("cubics")
                    if cubic_type == 'shared':
                        cubics = cubic
                        assigned_user = assigned_user[0]
                    else:
                        cubics = [cubic]
                    if all_assignments_are_okay(business_group, [assigned_user], cubics, cubic_type):
                        for assignment in AssignUserCubic.objects.filter(assigned_user=assigned_user):
                            assignment.delete()
                        for cubic in cubics:
                            assignment = AssignUserCubic(assigned_user=assigned_user, cubic=cubic)
                            assignment.save()
                            send_assign_notification(request.user.email, [assigned_user], cubics)
                        return redirect('focal_point:assignments')
                    else:
                        return render(request, 'focal_point/viewuserassignments.html',
                                      {'curr_user': wanted_user, 'error': 'Could not make assignment', 'form': form})
                else:
                    return render(request, 'focal_point/viewuserassignments.html',
                                  {'curr_user': wanted_user,'form': form})
        except ValueError:
            form = form_type(users_queryset=CustomUser.objects.filter(pk=user_id), business_group=business_group,
                             user_current_cubic=current_cubics_ids, data=request.POST or None)
            return render(request, 'focal_point/viewuserassignments.html',
                          {'curr_user': wanted_user, 'error': 'Bad info', 'form': form})


'''
See all assignments that a user has
'''
@user_is_focal_point
@user_in_focal_point_group
def view_all_user_assignments(request,user_id):
    wanted_user = CustomUser.objects.filter(pk=user_id)[0]
    wanted_user_assignments = AssignUserCubic.objects.filter(assigned_user=wanted_user)
    current_cubics = [assignment.cubic for assignment in wanted_user_assignments]
    focal_point = CustomUser.objects.filter(employee_number=request.user.employee_number, focal_point=True, business_group=wanted_user.business_group)[0]
    cubic_type = 'shared' if wanted_user.percentage == 'part_time' else 'private'
    return edit_assignments_for_user(request, user_id, focal_point, wanted_user, current_cubics, cubic_type)

@user_is_focal_point
@user_in_focal_point_group
def delete_all_user_assignments(request, user_id):
    wanted_user = CustomUser.objects.filter(pk=user_id)[0]
    for assignment in AssignUserCubic.objects.filter(assigned_user=wanted_user):
        assignment.delete()
    return redirect('focal_point:assignments')


def send_notification(request, request_content):
    sender_mail = "yaelAmitIndustrial@gmail.com" #TODO - change to real mail
    space_planners = CustomUser.objects.filter(space_planner=True)
    receiver_mail = [space_planner.email for space_planner in space_planners]
    subject = "Request for more space from {focal_point} representing group {business_group}"\
        .format(focal_point=request.user.email, business_group=request_content.business_group)
    content = "{username} requested more space for group {business_group}. \n".format(username=request.user.email, business_group=request_content.business_group)
    if request_content.full_time_employees_amount:
        content += "The group needs space for {num_full} full time employees. \n".format(num_full=request_content.full_time_employees_amount)
    if request_content.part_time_employees_amount:
        content += "The group needs space for {part_time} full time employees. \n".format(part_time=request_content.part_time_employees_amount)
    if request_content.business_group_near_by:
        content += "They need to be near the group:{business_group_near_by}.\n".format(business_group_near_by=request_content.business_group_near_by)
    if request_content.near_low_density_lab:
        content += "They need to be near low density lab.\n"
    if request_content.near_high_density_lab:
        content += "They need to be near high density lab.\n"
    if request_content.destination_date:
        content += "The due date for the request is {due_date}. \n".format(due_date=request_content.destination_date)
    content += "Thank you."
    # send_mail(subject, content, sender_mail, receiver_mail)


@user_is_focal_point
def create_request(request):
    my_business_group_id = request.user.business_group.id
    qs = BusinessGroup.objects.exclude(id=my_business_group_id).filter(admin_group=False)
    if request.method == 'GET':
        return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm(business_group_qs=qs)})
    else:
        try:
            if ((request.POST.get('full_time_employees_amount') == '' or request.POST.get('full_time_employees_amount') == '0')
                    and (request.POST.get('part_time_employees_amount') == '' or request.POST.get('part_time_employees_amount') == '0')
                    and (request.POST.get('business_group_near_by') == '')):
                return render(request, 'focal_point/createrequests.html',
                              {'form': FocalPointRequestForm(business_group_qs=qs),
                               'error': 'Cant submit empty form'})
            request_copy = request.POST.copy()
            request_copy['near_low_density_lab'] = True if request.POST.get('near_low_density_lab', False) == 'on' else False
            request_copy['near_high_density_lab'] = True if request.POST.get('near_high_density_lab', False) == 'on' else False
            request_copy['destination_date'] = datetime.datetime.strptime(request.POST.get('destination_date', ''), "%d/%m/%Y").strftime("%Y-%m-%d") if request.POST.get('destination_date') != '' else None

            request_copy['full_time_employees_amount'] = 0 if request.POST.get('full_time_employees_amount') == '' else request.POST.get('full_time_employees_amount')
            request_copy['part_time_employees_amount'] = 0 if request.POST.get(
                'part_time_employees_amount') == '' else request.POST.get('part_time_employees_amount')

            if request.POST.get('business_group_near_by') != '':
                request_copy['business_group_near_by'] = BusinessGroup.objects.filter(id=request.POST.get('business_group_near_by'))[0]
            else:
                request_copy['campus'] = None
            if request.POST.get('campus') != '':
                request_copy['campus'] = Campus.objects.filter(id=request.POST.get('campus'))[0]
            else:
                request_copy['campus'] = None
            if request.POST.get('building') != '0' and request.POST.get('building') != '':
                request_copy['building'] = Building.objects.filter(id=request.POST.get('building'))[0]
                print(request_copy['building'])
            else:
                request_copy['building'] = None
            if request.POST.get('floor') != '0' and request.POST.get('floor') != '':
                request_copy['floor'] = Floor.objects.filter(id=request.POST.get('floor'))[0]
                print(request_copy['floor'])
            else:
                request_copy['floor'] = None
            # form = FocalPointRequestForm(request_copy, business_group_qs=qs) // form was not working- maybe because of the added ajax.
            # new_request = form.save(commit=False)
            new_request = FocalPointRequest.objects.create(business_group=request.user.business_group,
                                                           full_time_employees_amount=request_copy['full_time_employees_amount'],
                                                           part_time_employees_amount=request_copy[
                                                               'part_time_employees_amount'],
                                                           business_group_near_by=request_copy['business_group_near_by'],
                                                           campus=request_copy['campus'],
                                                           building=request_copy['building'],
                                                           floor=request_copy['floor'],
                                                           near_low_density_lab=request_copy['near_low_density_lab'],
                                                           near_high_density_lab=request_copy['near_high_density_lab'],
                                                           destination_date=request_copy['destination_date'])
            # new_request.business_group = request.user.business_group
            # new_request.save()
            send_notification(request, new_request)
            return redirect('focal_point:myrequests')
        except ValueError:
            return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm(business_group_qs=qs),
                                                                    'error': 'Bad data passed in'})

@user_is_focal_point
def display_requests(request):
    users_in_focal_point_group = CustomUser.objects.filter(business_group=request.user.business_group)
    requests = RequestToChangeCubic.objects.filter(user__in=users_in_focal_point_group).order_by('request_date')
    table = UserRequestsTable(requests, template_name="django_tables2/bootstrap.html")
    RequestConfig(request, paginate={"per_page": 10, "page": 1}).configure(table)
    return render(request, 'focal_point/requests.html', {'table': table})


def send_change_status_notification(request, request_content):
    sender_mail = "yaelAmitIndustrial@gmail.com" #TODO - change to real mail
    focal_point = request.user.email
    receiver_mail = (request_content['user']).email
    subject = "Request to change cubic status update"
    content = "{focal_point} changed your request status to '{status}'".format(focal_point=focal_point, status=request_content['status'])
    # send_mail(subject, content,
    #           sender_mail,
    #           [receiver_mail])

@request_user_in_focal_point_group
@user_is_focal_point
def display_request(request, request_id):
    user_request = get_object_or_404(RequestToChangeCubic, pk=request_id)
    if request.method == 'GET':
        form = RequestToChangeCubicFocalPointForm(instance=user_request)
        return render(request, 'focal_point/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            request_copy = request.POST.copy()
            request_copy['user'] = user_request.user
            request_copy['cubic'] = user_request.cubic
            form = RequestToChangeCubicFocalPointForm(request_copy, instance=user_request)
            orig_request_status = user_request.status
            form.save()
            if request_copy['status'] != orig_request_status:
                send_change_status_notification(request, request_copy)
            return redirect('focal_point:requests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'Bad info', 'form': form})

@request_user_in_focal_point_group
@user_is_focal_point
def delete_user_request(request, request_id):
    curr_request = get_object_or_404(RequestToChangeCubic, pk=request_id)
    if request.method == 'POST':
        curr_request.delete()
        return redirect('focal_point:requests')


@user_is_focal_point
def display_my_requests(request):
    requests = FocalPointRequest.objects.filter(business_group=request.user.business_group)
    return render(request, 'focal_point/myrequests.html', {'requests': requests})


@user_is_focal_point_request_author
@user_is_focal_point
def display_my_request(request, request_id):
    my_business_group_id = request.user.business_group.id
    qs = BusinessGroup.objects.exclude(id=my_business_group_id, admin_group=True)
    user_request = get_object_or_404(FocalPointRequest, pk=request_id)
    if request.method == 'GET':
        form = FocalPointRequestForm(instance=user_request, business_group_qs=qs)
        return render(request, 'focal_point/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            request_copy = request.POST.copy()
            # if 'near_lab' in request.POST.keys():
            #     request_copy['near_lab'] = True
            # if 'near_conference_room' in request.POST.keys():
            #     request_copy['near_conference_room'] = True
            form = FocalPointRequestForm(request_copy, instance=user_request, business_group_qs=qs)
            curr_request = form.save(commit=False)
            #curr_request.focal_point = FocalPoint.objects.filter(custom_user=request.user)[0]
            curr_request.save()
            return redirect('focal_point:myrequests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'bad info', 'form': form})

@user_is_focal_point
def display_new_positions(request):
    positions_list = NewPosition.objects.filter(business_group=request.user.business_group).order_by('creation_date')
    positions_filter = PositionFilter(request.GET, queryset=positions_list)
    table = NewPositionTable(positions_filter.qs, template_name="django_tables2/bootstrap.html")
    table.exclude = ('business_group')
    RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
    return render(request, 'focal_point/newpositions.html', {'table': table, 'filter': positions_filter})





@user_is_focal_point_request_author
@user_is_focal_point
def delete_request(request, request_id):
    curr_request = get_object_or_404(FocalPointRequest, pk=request_id, business_group=request.user.business_group)
    if request.method == 'POST':
        curr_request.delete()
        return redirect('focal_point:myrequests')
