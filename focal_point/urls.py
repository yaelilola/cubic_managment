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
from django.contrib import admin
from django.urls import path
from focal_point import views as focal_point_views

app_name = 'focal_point'

urlpatterns = [
    path('requests/', focal_point_views.display_requests, name='requests'),
    path('viewrequest/<int:request_id>', focal_point_views.display_request, name='viewrequest'),
    path('createrequest/', focal_point_views.create_request, name='createRequest'),
    path('myrequests/', focal_point_views.display_my_requests, name='myrequests'),
    path('viewmyrequest/<int:request_id>', focal_point_views.display_my_request, name='viewmyrequest'),
    path('assign/', focal_point_views.assign, name='assign'),
    path('assignments/', focal_point_views.view_assignments, name='assignments'),
]
