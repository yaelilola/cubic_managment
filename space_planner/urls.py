"""cubic_managment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from space_planner import views as space_planner_views

app_name = 'space_planner'

urlpatterns = [
    path('requests/', space_planner_views.display_requests, name='requests'),
    path('viewrequest/<int:request_id>', space_planner_views.display_request, name='viewrequest'),
    path('assignfocalpoint/', space_planner_views.assign_focal_point, name='assignfocalpoint'),
    path('assign/', space_planner_views.assign_space, name='assign'),
    path('ajax/load-employees/', space_planner_views.load_employees, name='ajax_load_employees'),
    path('statistics/campuses/', space_planner_views.get_statistics, name='statistics'),
    path('statistics/campuses/<str:campus_id>/buildings', space_planner_views.get_building_table,
         name='get_building_table'),
    path('statistics/campuses/<str:campus_id>/buildings/<str:building_id>/floors', space_planner_views.get_floor_table,
         name='get_floor_table'),
    path('new_positions/', space_planner_views.display_new_positions, name='new_positions'),
    path('ajax/load-requests/', space_planner_views.load_requests, name='ajax_load_requests'),
]
