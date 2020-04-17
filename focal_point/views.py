from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from CustomRequests.forms import RequestToChangeCubicFocalPointForm, FocalPointRequestForm
from focal_point.models import FocalPoint
from assign.forms import AssignUserCubicForm
from assign.models import AssignUserCubic
from recruit.models import NewPosition
from custom_user.models import CustomUser
from facilities.models import Cubic

# Create your views here.
#foacl point actions

def view_assignments(request):
    focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
    assignments = AssignUserCubic.objects.filter(assigner=focal_point)
    return render(request, 'focal_point/assignments.html', {'assignments': assignments})

def assign(request):
    #TODO - add assignment logic
    focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
    users_queryset = CustomUser.objects.filter(business_group=focal_point.custom_user.business_group)
    cubics_queryset = Cubic.objects.filter(focal_point=focal_point)
    if request.method == 'GET':
        return render(request, 'focal_point/assign.html', {'form': AssignUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset)})
    else:
        try:
            focal_point = get_object_or_404(FocalPoint, custom_user=request.user)
            form = AssignUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset, data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    assigned_users = form.cleaned_data.get("users")
                    cubics = form.cleaned_data.get("cubics")
                    for user in assigned_users:
                        for cubic in cubics:
                            assignment = AssignUserCubic(assigner=focal_point, assigned_user=user, cubic=cubic)
                            assignment.save()
            return redirect('homepage')
        except ValueError:
            return render(request, 'focal_point/assign.html',
                          {'form': AssignUserCubicForm(users_queryset=users_queryset, cubics_queryset=cubics_queryset), 'error': 'Bad data passed in'})


def create_request(request):
    if request.method == 'GET':
        return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm()})
    else:
        try:
            form = FocalPointRequestForm(request.POST)
            form.save()
            return redirect('homepage')
        except ValueError:
            return render(request, 'focal_point/createrequests.html', {'form': FocalPointRequestForm(),
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
            form = RequestToChangeCubicFocalPointForm(request.POST, instance=user_request)
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
    user_request = get_object_or_404(FocalPointRequest, pk=request_id)
    if request.method == 'GET':
        form = FocalPointRequestForm(instance=user_request)
        return render(request, 'focal_point/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            form = RequestToChangeCubicFocalPointForm(request.POST, instance=user_request)
            curr_request = form.save(commit=False)
            curr_request.focal_point = request.user
            curr_request.save()
            return redirect('focal_point:myrequests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'Bad info', 'form': form})


def display_new_positions(request):
    new_positions = NewPosition.objects.all()
    return render(request, 'focal_point/newpositions.html', {'positions': new_positions})
