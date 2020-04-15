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
from custom_user import views as custom_user_views

urlpatterns = [
    path('mycubic/', custom_user_views.get_my_cubic, name='mycubic'),
    path('searchcubic/<user_email>', custom_user_views.search_user_cubic, name='searchcubic'),
    path('createrequest', custom_user_views.ask_to_change_cubic, name='createrequest'),
]
