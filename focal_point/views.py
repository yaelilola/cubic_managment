from django.shortcuts import render, get_object_or_404, redirect
from CustomRequests.models import RequestToChangeCubic
from CustomRequests.forms import RequestToChangeCubicFocalPointForm

# Create your views here.
#foacl point actions
def assign_user(request):
    pass


def create_request(request):
    pass


def display_requests(request):
    requests = RequestToChangeCubic.objects.all()
    return render(request, 'focal_point/requests.html', {'requests': requests})


def display_request(request, request_id):
    user_request = get_object_or_404(RequestToChangeCubic, pk=request_id)
    print(user_request)
    if request.method == 'GET':
        form = RequestToChangeCubicFocalPointForm(instance=user_request)
        return render(request, 'focal_point/viewrequest.html', {'request': user_request, 'form': form})
    else:
        try:
            form = RequestToChangeCubicFocalPointForm(request.POST, instance=user_request)
            form.save()
            return redirect('requests')
        except ValueError:
            return render(request, 'focal_point/viewrequest.html',
                          {'request': user_request, 'error': 'Bad info', 'form': form})
