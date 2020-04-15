from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from custom_user.forms import CustomUserSignUpForm
from custom_user.models import CustomUser, BusinessGroup


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
        focal_point = False
        space_planner = False
        if request.POST['focal_point']:
            focal_point = True
        if request.POST['space_planner']:
            space_planner = True
        try:
            user = CustomUser.objects.create_user(request.POST['email'],
                                                  employee_number=request.POST['employee_number'],
                                                  focal_point=focal_point,
                                                  space_planner=space_planner,
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
    # if request.method == 'POST':
    #     logout(request)
    #     return redirect('home')
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


def get_my_cubic(request):
    pass


def ask_to_change_cubic(request):
    pass


def search_user_cubic(request):
    pass


def get_business_group(request):
    pass




