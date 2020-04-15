from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from custom_user.forms import CustomUserSignUpForm
from custom_user.models import CustomUser, BusinessGroup
from assign.models import AssignUserCubic


def homepage(request):
    return render(request, 'custom_user/homepage.html')

# Create your views here.
#Todo: change forms, check id doesnot exist, check space planner or focal point does this?
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'custom_user/signupuser.html', {'form': CustomUserSignUpForm()})
    else:
        # create a new user
        # if request.POST['password1'] == request.POST['password2']:
        try:
            user = CustomUser.objects.create_user(request.POST['email'],
                                                  employee_number=request.POST['employee_number'],
                                                  focal_point=request.POST.get('focal_point', False),
                                                  space_planner=request.POST.get('space_planner', False),
                                                  percentage=request.POST['percentage'],
                                                  business_group=BusinessGroup(request.POST['business_group']),
                                                  password=request.POST['password'])
            #TODO - add start date and end date handling
            user.save()
            login(request, user)
            return redirect('homepage')
        except IntegrityError:
            return render(request, 'custom_user/signupuser.html',
                          {'form': CustomUserSignUpForm(), 'error': 'That username/employee number is already taken. Please choose a new one'})
    # else:
    #     return render(request, 'custom_user/signupuser.html',
    #                   {'form': CustomUserSignUpForm(), 'error': 'Password did not match'})


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
    pass


@login_required()
def search_user_cubic(request, user_email):
    user = get_object_or_404(CustomUser, email=user_email)
    assignments = AssignUserCubic.objects.filter(assigned_user=user)
    return render(request, 'custom_user/otherscubics.html',
                  {'assignments': assignments})





