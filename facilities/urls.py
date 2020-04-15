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
from facilities import views as facilities_views

app_name = 'facilities'

urlpatterns = [
    path('campuses/', facilities_views.display_campueses, name='campuses'),
    path('viewcampus/<campus_id>', facilities_views.display_campues, name='viewcampus'),
    path('buildings/', facilities_views.display_buildings, name='buildings'),
    path('viewbuilding/<building_id>', facilities_views.display_building, name='viewbuilding')
]
