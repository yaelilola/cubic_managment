from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser

# Create your views here.
#Todo: change forms, check id doesnot exist, check space planner or focal point does this?
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'custom_user/signupuser.html', {'form': UserCreationForm()})
    else:
        # create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser(User.objects.create_user(request.POST['username'], password=request.POST['password1']))
                user.type = request.POST['type']
                user.id = request.POST['id']
                if request.POST['end_date']:
                    user.end_date = request.POST['end_date']
                if request.POST['start_date']:
                    user.end_date = request.POST['start_date']
                user.save()
                login(request, user)
                return redirect('homepage')
            except IntegrityError:
                return render(request, 'custom_user/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'That username/id is already taken. Please choose a new one'})
        else:
            return render(request, 'custom_user/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


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





