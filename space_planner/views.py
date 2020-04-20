from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import FocalPointRequest
from CustomRequests.forms import FocalPointRequestSpacePlannerForm
from assign.forms import AssignSpacesToBusinessGroupsForm
from facilities.models import Cubic
from custom_user.models import CustomUser,BusinessGroup
from focal_point.models import FocalPoint
from .forms import ChooseFocalPointForm

#space planner actions
def simulations(request):
    pass


def get_alerts(request):
    pass


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
                    try:
                        focal_point = FocalPoint.objects.filter(custom_user=
                                                               (CustomUser.objects.filter(focal_point=True,
                                                                                          business_group=business_group))[0])[0]

                    except ValueError:
                        return render(request, 'space_planner/assignspace.html',
                                      {'error': 'No focal point', 'form': AssignSpacesToBusinessGroupsForm()})
                    spaces = form.cleaned_data.get("spaces")
                    for space in spaces:
                        cubics = Cubic.objects.filter(space=space)
                        for cubic in cubics:
                            cubic.set_focal_point(focal_point)
                            cubic.save()
            return redirect('homepage')
        except ValueError:
            return render(request, 'space_planner/assignspace.html',
                          {'error': 'Bad info', 'form': AssignSpacesToBusinessGroupsForm()})



def get_statistics(request):
    pass


def display_requests(request):
    requests = FocalPointRequest.objects.all()
    return render(request, 'space_planner/requests.html', {'requests': requests})


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


def assign_focal_point(request):
    if request.method == 'GET':
        return render(request, 'space_planner/assign_focal_point.html', {'form': ChooseFocalPointForm()})
    else:
        try:
            if request.POST:
                chosen_business_group_query_set = BusinessGroup.objects.filter(id=request.POST.get('business_group'))
                chosen_employee_query_set = CustomUser.objects.filter(email=request.POST.get('employee'))
                chosen_employee = chosen_employee_query_set[0]  # should be only one
                try:
                    old_focal_point = CustomUser.objects.filter(business_group=chosen_business_group_query_set[0],focal_point=True)[0]
                    old_focal_point.focal_point = False
                    old_focal_point.save()
                    old_focal_point_as_focal_point = FocalPoint.objects.filter(custom_user=old_focal_point)[0]
                    old_focal_point_as_focal_point.delete()
                except IndexError:
                    pass
                chosen_employee.focal_point = True
                chosen_employee.save()
                FocalPoint.objects.create(custom_user=chosen_employee)
                return redirect('homepage')
        except ValueError:
            return render(request, 'space_planner/assign_focal_point.html',
                          {'form': ChooseFocalPointForm(), 'error': 'Bad info'})



def load_employees(request):
    chosen_business_group = request.GET.get('business_group')
    employees = CustomUser.objects.filter(business_group=chosen_business_group)
    return render(request, 'space_planner/employees_dropdown_list_options.html', {'employees': employees})



