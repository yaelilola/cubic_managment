from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import FocalPointRequest
from CustomRequests.forms import FocalPointRequestSpacePlannerForm
#space planner actions
def simulations(request):
    pass


def get_alerts(request):
    pass


def assign_space(request):
    pass


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

