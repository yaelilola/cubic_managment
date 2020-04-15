from django.shortcuts import render, get_object_or_404
from facilities.models import Campus, Building, Floor, Space, Cubic
# Create your views here.

def display_campueses(request):
    campuses = Campus.objects.all()
    return render(request, 'facilities/list.html', {'title': 'Campuses', 'items': campuses,
                                                    'function_name': 'viewcampus'})

def display_campues(request, campus_id):
    wanted_campus = get_object_or_404(Campus, id=campus_id)
    buildings = Building.objects.filter(campus=wanted_campus)
    return render(request, 'facilities/list.html', {'title': 'Campuses' + str(campus_id), 'items': buildings,
                                                    'function_name': 'viewcampus'})
