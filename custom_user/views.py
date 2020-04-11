from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from custom_user.forms import CustomUserSignUpForm
from custom_user.models import CustomUser, Unit


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
            user = CustomUser.objects.create_user(request.POST['email'],employee_number=request.POST['employee_number'],
                                                  type=request.POST['type'],
                                                  percentage=request.POST['percentage'],
                                                  unit=Unit(request.POST['unit']),
                                                  password=request.POST['password'])
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
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def get_my_cubic(request):
    pass


def ask_to_change_cubic(request):
    pass


def search_user_cubic(request):
    pass





