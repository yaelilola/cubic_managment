from django.core.exceptions import PermissionDenied
from CustomRequests.models import RequestToChangeCubic, FocalPointRequest
from custom_user.models import CustomUser

def user_is_focal_point(function):
    def wrap(request, *args, **kwargs):
        if request.user.focal_point:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_space_planner(function):
    def wrap(request, *args, **kwargs):
        if request.user.space_planner:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_request_author(function):
    def wrap(request, *args, **kwargs):
        request_to_change_cubic = RequestToChangeCubic.objects.get(pk=kwargs['request_id'])
        if request_to_change_cubic.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_focal_point_request_author(function):
    def wrap(request, *args, **kwargs):
        focal_point_request = FocalPointRequest.objects.get(pk=kwargs['request_id'])
        if focal_point_request.business_group == request.user.business_group:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_in_focal_point_group(function):
    def wrap(request, *args, **kwargs):
        user_group = (CustomUser.objects.get(pk=kwargs['user_id'])).business_group
        focal_point_group = request.user.business_group
        if user_group == focal_point_group:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


"""
The user who requested to change the sit is in the focal point group
"""
def request_user_in_focal_point_group(function):
    def wrap(request, *args, **kwargs):
        user_group = ((RequestToChangeCubic.objects.get(pk=kwargs['request_id'])).user).business_group
        focal_point_group = request.user.business_group
        if user_group == focal_point_group:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap