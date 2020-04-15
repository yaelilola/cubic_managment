from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from CustomRequests.forms import RequestToChangeCubicFocalPointForm, FocalPointRequestForm
from focal_point.models import FocalPoint

# Create your views here.
#foacl point actions
def assign_user(request):
    pass


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
