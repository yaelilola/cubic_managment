from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import FocalPointRequest
from CustomRequests.forms import FocalPointRequestSpacePlannerForm
from assign.forms import AssignSpacesToBusinessGroupsForm
from facilities.models import Cubic
from custom_user.models import CustomUser, BusinessGroup
from .forms import ChooseFocalPointForm
from cubic_managment.decorators import user_is_space_planner

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


@user_is_space_planner
def get_statistics(request):
    pass

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



