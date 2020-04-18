from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from CustomRequests.forms import RequestToChangeCubicFocalPointForm, FocalPointRequestForm
from focal_point.models import FocalPoint
from assign.forms import AssignPartTimeUserCubicForm, AssignFullTimeUserCubicForm
from assign.models import AssignUserCubic
from recruit.models import NewPosition
from custom_user.models import CustomUser, BusinessGroup
from facilities.models import Cubic

# Create your views here.
#foacl point actions

def view_assignments(request):
    focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
    assignments = AssignUserCubic.objects.filter(assigner=focal_point)
    users = CustomUser.objects.filter(business_group=request.user.business_group)
    return render(request, 'focal_point/assignments.html', {'assignments': assignments, 'users': users})


def is_cubic_available(cubic, person_amount=1):
    if cubic.type == 'private':
        if len(AssignUserCubic.objects.filter(cubic=cubic)) < 1 and person_amount == 1:
            return True
        else:
            return False
    else:
    #should be shared
        if len(AssignUserCubic.objects.filter(cubic=cubic))+person_amount <= 3:
            return True
        else:
            return False


def get_available_cubics(focal_point, person_amount=1, cubic_type='private'):
    cubics_queryset_aux = Cubic.objects.filter(focal_point=focal_point, type=cubic_type)
    cubics_queryset = cubics_queryset_aux
    for cubic in cubics_queryset_aux:
        if is_cubic_available(cubic, person_amount)is False:
            cubics_queryset = cubics_queryset.exclude(id=cubic.id)
    return cubics_queryset


def all_assignments_are_okay(focal_point,assigned_users, cubics, cubic_type='private'):
    for cubic in cubics:
        cubics_users = [assignment.assigned_user for assignment in AssignUserCubic.objects.filter(cubic=cubic)]
        users_not_in_cubic = [user for user in assigned_users if user not in cubics_users]
        available_cubics = get_available_cubics(focal_point, len(users_not_in_cubic), cubic_type)
        if cubic not in available_cubics:
            return False
    return True


def assign_part_time(request):
    #TODO - add assignment logic: should we use ajax, or check in backend?
    focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
    users_queryset = CustomUser.objects.filter(business_group=focal_point.custom_user.business_group, percentage='part_time')
    cubics_queryset = get_available_cubics(focal_point, 1, 'shared')
    if request.method == 'GET':
        return render(request, 'focal_point/assign.html',
                      {'form': AssignPartTimeUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset)})
    else:
        try:
            form = AssignPartTimeUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset, data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_users = form.cleaned_data.get("users")
                    cubics = form.cleaned_data.get("cubics")
                    if all_assignments_are_okay(focal_point, assigned_users, cubics, 'shared'):
                        for user in assigned_users:
                            for cubic in cubics:
                                try:
                                    assignment = AssignUserCubic(assigner=focal_point, assigned_user=user, cubic=cubic)
                                    assignment.save()
                                except Exception as e:
                                    if str(e).startswith('UNIQUE constraint failed'):
                                        pass
                    else:
                        return render(request, 'focal_point/assign.html',
                                      {'form': AssignPartTimeUserCubicForm(users_queryset=users_queryset,
                                                                           cubics_queryset=cubics_queryset),
                                       'error': 'There is not enough place in the selected cubics'})
            return redirect('focal_point:assignments')
        except ValueError:
            return render(request, 'focal_point/assign.html',
                          {'form': AssignPartTimeUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset), 'error': 'Bad data passed in'})


def assign_full_time(request):
    focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
    full_time_users = CustomUser.objects.filter(business_group=focal_point.custom_user.business_group, percentage='full_time')
    full_not_assigned_time_users_id = [user.id for user in full_time_users if len(AssignUserCubic.objects.filter(assigned_user=user)) == 0]
    users_queryset = CustomUser.objects.filter(id__in=full_not_assigned_time_users_id)
    cubics_queryset = get_available_cubics(focal_point)
    if request.method == 'GET':
        return render(request, 'focal_point/assign.html',
                      {'form': AssignFullTimeUserCubicForm(users_queryset=users_queryset,
                                                           cubics_queryset=cubics_queryset)})
    else:
        try:
            form = AssignFullTimeUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset,
                                               data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_user = form.cleaned_data.get("user")
                    cubic = form.cleaned_data.get("cubic")
                    print(cubic.type)
                    print(assigned_user)
                    if all_assignments_are_okay(focal_point, [assigned_user], [cubic], 'private'):
                        try:
                            assignment = AssignUserCubic(assigner=focal_point, assigned_user=assigned_user, cubic=cubic)
                            assignment.save()
                        except Exception as e:
                            if str(e).startswith('UNIQUE constraint failed'):
                                pass
                    else:
                        return render(request, 'focal_point/assign.html',
                                      {'form': AssignFullTimeUserCubicForm(users_queryset=users_queryset,
                                                                           cubics_queryset=cubics_queryset),
                                       'error': 'Could not make assignment'})
            return redirect('focal_point:assignments')
        except ValueError:
            return render(request, 'focal_point/assign.html',
                          {'form': AssignFullTimeUserCubicForm(users_queryset=users_queryset,
                                                               cubics_queryset=cubics_queryset),
                           'error': 'Bad data passed in'})


def edit_assignments_part_time(request,user_id,focal_point,wanted_user,wanted_user_assignments,current_cubics):
    if request.method == 'GET':
        #TODO: think which cubics should be seen
        available_cubics = get_available_cubics(focal_point, 1, 'shared')
        available_cubics_ids = [cubic.id for cubic in available_cubics]
        current_cubics_ids = [cubic.id for cubic in current_cubics]
        cubics_queryset = Cubic.objects.filter(id__in=(available_cubics_ids+current_cubics_ids))
        form = AssignPartTimeUserCubicForm(users_queryset=CustomUser.objects.filter(pk=user_id), cubics_queryset=cubics_queryset,
                                           initial={'cubics': current_cubics,'users': wanted_user})
        return render(request, 'focal_point/viewuserassignments.html', {'curr_user': wanted_user, 'form': form})

    else:
        try:
            form = AssignPartTimeUserCubicForm(users_queryset=CustomUser.objects.all(), cubics_queryset=Cubic.objects.all(),
                                               data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_user = form.cleaned_data.get("users")
                    cubics = form.cleaned_data.get("cubics")
                    if all_assignments_are_okay(focal_point,[assigned_user],cubics,'shared'):
                        for user in [assigned_user]:
                            for assignment in AssignUserCubic.objects.filter(assigned_user=user):
                                assignment.delete()
                            for cubic in cubics:
                                assignment = AssignUserCubic(assigner=focal_point, assigned_user=user, cubic=cubic)
                                assignment.save()
                        return redirect('focal_point:assignments')
                    else:
                        return render(request, 'focal_point/viewuserassignments.html',
                                      {'curr_user': wanted_user, 'error': 'There is not enough place in the selected cubics', 'form': form})
        except ValueError:
            return render(request, 'focal_point/viewuserassignments.html',
                          {'curr_user': wanted_user, 'error': 'Bad info', 'form': form})

def  edit_assignments_full_time(request,user_id,focal_point,wanted_user,wanted_user_assignments,current_cubics):
    if request.method == 'GET':
        available_cubics = get_available_cubics(focal_point, 1, 'private')
        available_cubics_ids = [cubic.id for cubic in available_cubics]
        # TODO: we assumed that if the user is full time, it has only one assignment
        current_cubics_ids = [cubic.id for cubic in current_cubics]
        cubics_queryset = Cubic.objects.filter(id__in=(available_cubics_ids + current_cubics_ids))
        form = AssignFullTimeUserCubicForm(users_queryset=CustomUser.objects.filter(pk=user_id)
                                           , cubics_queryset=cubics_queryset,
                                           initial={'cubic': current_cubics,
                                                    'user': wanted_user})
        return render(request, 'focal_point/viewuserassignments.html', {'curr_user': wanted_user, 'form': form})

    else:
        try:
            form = AssignFullTimeUserCubicForm(users_queryset=CustomUser.objects.all(), cubics_queryset=Cubic.objects.all(),
                                               data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_user = form.cleaned_data.get("users")
                    cubic = form.cleaned_data.get("cubics")
                    if all_assignments_are_okay(focal_point,[assigned_user],[cubic],'shared'):
                        for user in [assigned_user]:
                            for assignment in AssignUserCubic.objects.filter(assigned_user=user):
                                assignment.delete()
                            for cubic in [cubic]:
                                assignment = AssignUserCubic(assigner=focal_point, assigned_user=user, cubic=cubic)
                                assignment.save()
                        return redirect('focal_point:assignments')
                    else:
                        return render(request, 'focal_point/viewuserassignments.html',
                                      {'curr_user': wanted_user, 'error': 'Could not make assignment', 'form': form})
        except ValueError:
            return render(request, 'focal_point/viewuserassignments.html',
                          {'curr_user': wanted_user, 'error': 'Bad info', 'form': form})

def view_all_user_assignments(request,user_id):
    wanted_user = CustomUser.objects.filter(pk=user_id)[0]
    wanted_user_assignments = AssignUserCubic.objects.filter(assigned_user=wanted_user)
    current_cubics = [assignment.cubic for assignment in wanted_user_assignments]
    focal_point = FocalPoint.objects.filter(custom_user=request.user)[0]
    if wanted_user.percentage=='part_time':
        return edit_assignments_part_time(request,user_id,focal_point,wanted_user,wanted_user_assignments,current_cubics)
    else:
        return edit_assignments_full_time(request,user_id,focal_point,wanted_user,wanted_user_assignments,current_cubics)

def delete_all_user_assignments(request,user_id):
    wanted_user = CustomUser.objects.filter(pk=user_id)[0]
    for assignment in AssignUserCubic.objects.filter(assigned_user=wanted_user):
        assignment.delete()
    return redirect('focal_point:assignments')


def create_request(request):
    my_business_group_id = request.user.business_group.id
    qs = BusinessGroup.objects.exclude(id=my_business_group_id)
    if request.method == 'GET':
        return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm(business_group_qs=qs)})
    else:
        try:
            if ((request.POST['size'] == '' or request.POST['size'] == '0') and
                (request.POST['business_group_near_by'] == '') and
                ('near_lab' not in request.POST.keys()) and
                ('near_conference_room' not in request.POST.keys())):
                return render(request, 'focal_point/createrequests.html',
                              {'form': FocalPointRequestForm(business_group_qs=qs),
                               'error': 'Cant submit empty form'})
            request_copy = request.POST.copy()
            if 'near_lab' in request.POST.keys():
                request_copy['near_lab'] = True
            if 'near_conference_room' in request.POST.keys():
                request_copy['near_conference_room'] = True
            form = FocalPointRequestForm(request_copy, business_group_qs=qs)
            new_request = form.save(commit=False)
            new_request.focal_point = FocalPoint.objects.filter(custom_user=request.user)[0]
            new_request.business_group = request.user.business_group
            new_request.save()
            return redirect('focal_point:myrequests')
        except ValueError:
            return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm(business_group_qs=qs),
                                                                    'error': 'Bad data passed in'})


def display_requests(request):
    requests = RequestToChangeCubic.objects.all()
    return render(request, 'focal_point/requests.html', {'requests': requests})


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
            form.save()
            return redirect('focal_point:requests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'Bad info', 'form': form})


def display_my_requests(request):
    user = get_object_or_404(FocalPoint, custom_user=request.user)
    requests = FocalPointRequest.objects.filter(focal_point=user)
    return render(request, 'focal_point/myrequests.html', {'requests': requests})


def display_my_request(request, request_id):
    my_business_group_id = request.user.business_group.id
    qs = BusinessGroup.objects.exclude(id=my_business_group_id)
    user_request = get_object_or_404(FocalPointRequest, pk=request_id)
    if request.method == 'GET':
        form = FocalPointRequestForm(instance=user_request, business_group_qs=qs)
        return render(request, 'focal_point/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            request_copy = request.POST.copy()
            if 'near_lab' in request.POST.keys():
                request_copy['near_lab'] = True
            if 'near_conference_room' in request.POST.keys():
                request_copy['near_conference_room'] = True
            form = FocalPointRequestForm(request_copy, instance=user_request, business_group_qs=qs)
            curr_request = form.save(commit=False)
            #curr_request.focal_point = FocalPoint.objects.filter(custom_user=request.user)[0]
            curr_request.save()
            return redirect('focal_point:myrequests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'bad info', 'form': form})


def display_new_positions(request):
    new_positions = NewPosition.objects.filter(business_group=request.user.business_group).order_by('creation_date')
    return render(request, 'focal_point/newpositions.html', {'positions': new_positions})


def delete_request(request, request_id):
    curr_request = get_object_or_404(FocalPointRequest, pk=request_id, business_group=request.user.business_group)
    if request.method == 'POST':
        curr_request.delete()
        return redirect('focal_point:myrequests')
