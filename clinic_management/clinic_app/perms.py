from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import User
from django.contrib.contenttypes.models import ContentType

class IsSelf(IsAuthenticated):
    """
    Permission class that allows access only if the user making the request
    is the same as the object being accessed.

    Extends:
        IsAuthenticated

    Methods:
        has_object_permission(request, view, obj):
            Check if the request user is the same as the object being accessed.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user is the same as the object being accessed.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.
            obj (django.db.models.Model): The object being accessed.

        Returns:
            bool: True if the request user is the same as the object being accessed,
                  False otherwise.
        """
        return request.user.id == obj.id

    
    
class IsPatientUser(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user belongs
    to a group with the appropriate permissions for the request method.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user belongs to a group with appropriate permissions.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user belongs to a group with appropriate permissions.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user belongs to a group with appropriate permissions,
                  False otherwise.
        """
        group = request.user.groups.first()
        
        content_type = ContentType.objects.get_for_model(User)
        
        if request.method == 'GET':
            return group.permissions.filter(content_type=content_type, codename ='view_user').exists()       
        else : 
            return group.permissions.filter(content_type=content_type, codename ='change_user').exists()         


class IsDoctor(IsAuthenticated):
    """

    Args:
        IsAuthenticated (_type_): _description_
    """    
    def has_permission(self, request, view):
        """_summary_

        Args:
            request (_type_): _description_
            view (_type_): _description_

        Returns:
            _type_: _description_
        """        
        if request.user.groups.filter(name = "Doctor").exists() and  request.user.is_doctor:
            return True
    
class IsNurse(IsAuthenticated):
    def has_permission(self, request, view):
        #   """
        #   Permission check for doctor
        #   """   
        if request.user.groups.filter(name = "Nurse").exists() and request.user.is_nurse:
            return True
    