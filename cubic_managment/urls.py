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
from django.urls import path, include
from custom_user import views as custom_user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('custom_user/', include('custom_user.urls')),
    path('signup/', custom_user_views.signupuser, name='signupuser'),
    path('logout/', custom_user_views.logoutuser, name='logoutuser'),
    path('login/', custom_user_views.loginuser, name='loginuser'),
    path('', custom_user_views.homepage, name='homepage'),
    path('users/', include('custom_user.urls')),
    path('focal_point/', include('focal_point.urls')),
    path('space_planner/', include('space_planner.urls')),
    path('facilities/', include('facilities.urls')),

]
