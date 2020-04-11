from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from custom_user.forms import CustomUserSignUpForm

# Create your views here.
#Todo: change forms, check id doesnot exist, check space planner or focal point does this?
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'custom_user/signupuser.html', {'form': CustomUserSignUpForm()})
    else:
        # create a new user
        # if request.POST['password1'] == request.POST['password2']:
        try:
            #user = CustomUser(User.objects.create_user(request.POST['username'], password=request.POST['password']))
            form = CustomUserSignUpForm(request.POST)
            user = form.save(commit=False)
            user.username = ""
            user.firstname = ""
            user.lastname = ""
            user.email = ""
            user.is_active = True
            user.is_superuser = False
            # user.type = request.POST['type']
            # user.id = request.POST['id']
            # if request.POST['end_date']:
            #     user.end_date = request.POST['end_date']
            # if request.POST['start_date']:
            #     user.end_date = request.POST['start_date']
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





