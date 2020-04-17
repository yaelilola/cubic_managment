from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from custom_user.forms import CustomUserSignUpForm, SearchUserCubicForm
from custom_user.models import CustomUser, BusinessGroup
from assign.models import AssignUserCubic
from CustomRequests.forms import RequestToChangeCubicForm
from CustomRequests.models import RequestToChangeCubic
from focal_point.models import FocalPoint
from facilities.models import Cubic
from django.db.models import Q


def homepage(request):
    return render(request, 'custom_user/homepage.html')

# Create your views here.
#Todo: change forms, check id doesnot exist, check space planner or focal point does this?
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'custom_user/signupuser.html', {'form': CustomUserSignUpForm()})
    else:
        # create a new user
        if request.POST['password'] == request.POST['password2']:
            focal_point = CustomUser.objects.filter(focal_point=True, business_group=request.POST['business_group'])
            if request.POST.get('focal_point', False) == 'on' and focal_point:
                return render(request, 'custom_user/signupuser.html',
                              {'form': CustomUserSignUpForm(), 'error': 'Focal point for this business group already exists'})
            else:
                try:
                    user = CustomUser.objects.create_user(request.POST['email'],
                                                          employee_number=request.POST['employee_number'],
                                                          focal_point=True if request.POST.get('focal_point', False) == 'on' else False,
                                                          space_planner=True if request.POST.get('space_planner', False) == 'on' else False,
                                                          percentage=request.POST['percentage'],
                                                          business_group=BusinessGroup(request.POST['business_group']),
                                                          password=request.POST['password'],)
                    #TODO - add start date and end date handling
                    user.save()
                    focal_point = FocalPoint(custom_user=user)
                    focal_point.save()
                    login(request, user)
                    return redirect('homepage')
                except IntegrityError:
                    return render(request, 'custom_user/signupuser.html',
                                  {'form': CustomUserSignUpForm(), 'error': 'That username/employee number is already taken. Please choose a new one'})
        else:
            return render(request, 'custom_user/signupuser.html',
                          {'form': CustomUserSignUpForm(), 'error': 'Password did not match'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    pass


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'custom_user/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'custom_user/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('homepage')
    pass

@login_required()
def get_my_cubic(request):
    assignments = AssignUserCubic.objects.filter(assigned_user=request.user)
    return render(request, 'custom_user/mycubic.html',
                  {'assignments': assignments})


@login_required()
def ask_to_change_cubic(request):
    my_assignments = AssignUserCubic.objects.filter(assigned_user=request.user)
    my_cubics_ids = [assignment.cubic.id for assignment in my_assignments]
    all_other_cubics = Cubic.objects.exclude(id__in=my_cubics_ids)

    if request.method == 'GET':
        return render(request, 'custom_user/changeCubic.html', {'form': RequestToChangeCubicForm(cubics_queryset=all_other_cubics)})
    else:
        try:
            form = RequestToChangeCubicForm(cubics_queryset=all_other_cubics, data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    wanted_cubic = form.cleaned_data.get("cubic")
                    reason = form.cleaned_data.get("reason")
                    newRequest = RequestToChangeCubic(user=request.user, cubic=wanted_cubic, reason=reason)
                    newRequest.save()
            return redirect('custom_user:requests')
        except ValueError:
            return render(request, 'custom_user/changeCubic.html', {'form': RequestToChangeCubicForm(cubics_queryset=all_other_cubics),
                                                                    'error': 'Bad data passed in'})


@login_required()
def search_user_cubic(request):
    if request.method == 'GET':
        return render(request, 'custom_user/otherscubics.html', {'form': SearchUserCubicForm()})
    else:
        try:
            form = SearchUserCubicForm(data=request.POST or None)
            if request.POST:
                if form.is_valid():
                    wanted_user = form.cleaned_data.get("user")
                    assignments = AssignUserCubic.objects.filter(assigned_user=wanted_user)
                    if len(assignments) != 0:
                        return render(request, 'custom_user/otherscubics.html', {'form': SearchUserCubicForm(),
                                                                             'assignments': assignments})
                    else:
                        return render(request, 'custom_user/otherscubics.html', {'form': SearchUserCubicForm(),
                                                                                 'error': 'no assignments'})
        except ValueError:
            return render(request, 'custom_user/otherscubics.html',
                          {'form': SearchUserCubicForm(), 'error': 'Bad info'})

@login_required()
def display_requests(request):
    requests = RequestToChangeCubic.objects.filter(user=request.user)
    return render(request, 'custom_user/requests.html', {'requests': requests})


def display_request(request, request_id):
    user_request = get_object_or_404(RequestToChangeCubic, pk=request_id)
    my_assignments = AssignUserCubic.objects.filter(assigned_user=request.user)
    my_cubics_ids = [assignment.cubic.id for assignment in my_assignments]
    all_other_cubics = Cubic.objects.exclude(id__in=my_cubics_ids)
    if request.method == 'GET':
        form = RequestToChangeCubicForm(cubics_queryset=all_other_cubics, initial={'cubic': user_request.cubic,
                                                                                   'reason': user_request.reason})
        return render(request, 'custom_user/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            current_request = RequestToChangeCubic.objects.filter(id=request_id)[0]
            form = RequestToChangeCubicForm(cubics_queryset=all_other_cubics, data=request.POST)
            if request.POST:
                if form.is_valid():
                    wanted_cubic = form.cleaned_data.get("cubic")
                    reason = form.cleaned_data.get("reason")
                    current_request.cubic = wanted_cubic
                    current_request.reason = reason
                    current_request.save(update_fields=['cubic', 'reason'])
            return redirect('custom_user:requests')
        except ValueError:
            return render(request, 'custom_user/viewrequest.html',
                          {'request': user_request, 'error': 'Bad info', 'form': form})


@login_required
def delete_request(request, request_id):
    curr_request = get_object_or_404(RequestToChangeCubic, pk=request_id, user=request.user)
    if request.method == 'POST':
        curr_request.delete()
        return redirect('custom_user:requests')





