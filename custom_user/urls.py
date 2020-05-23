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
from django.urls import path,reverse
from django.conf.urls import url
from custom_user import views as custom_user_views
from custom_user.views import CustomUserAutocomplete

app_name = 'custom_user'

urlpatterns = [
    path('mycubic/', custom_user_views.get_my_cubic, name='mycubic'),
    path('searchcubic/', custom_user_views.search_user_cubic, name='searchcubic'),
    path('createrequest', custom_user_views.ask_to_change_cubic, name='createrequest'),
    path('requests/', custom_user_views.display_requests, name='requests'),
    path('viewrequest/<int:request_id>', custom_user_views.display_request, name='viewrequest'),
    path('viewrequest/<int:request_id>/delete', custom_user_views.delete_request, name='deleterequest'),
    path('customuser-autocomplete/', CustomUserAutocomplete.as_view(), name='customuser-autocomplete'),
]
