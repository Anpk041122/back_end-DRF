from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from .models import (
    User, Patient, Employee, 
    MedicalHistory, Appointment, Order,
    OrderDetail, Schedule, ScheduleDetail,
    Medicine, Category,
)
from django.contrib.contenttypes.models import ContentType
from oauth2_provider.models import AccessToken

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

class IsCustomerPatient(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user belongs
    to a group with the appropriate permissions for the request method related to patients.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user belongs to a group with appropriate permissions.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user belongs to a group with appropriate permissions for patient.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user belongs to a group with appropriate permissions for patient,
                  False otherwise.
        """
        group = request.user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Patient)
        
        if request.method == 'GET':
            return group.permissions.filter(content_type=content_type, codename ='view_patient').exists()       
        else : 
            return group.permissions.filter(content_type=content_type, codename ='change_patient').exists() 

class IsEmployee(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and belongs to a group with the appropriate permissions to view employees.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and belongs to a group
            with the appropriate permissions to view employees.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and belongs to a group
        with the appropriate permissions to view employees.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and belongs to a group
                  with the appropriate permissions to view employees, False otherwise.
        """
        
        user = User.objects.get(id = request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Employee)
        
        return  group.permissions.filter(content_type=content_type, codename ='view_employee').exists()
        

class IsDoctorMedicalHistory(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and belongs to a group with the appropriate permissions to view medical histories.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and belongs to a group
            with the appropriate permissions to view medical histories.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and belongs to a group
        with the appropriate permissions to view medical histories.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and belongs to a group
                  with the appropriate permissions to view medical histories, False otherwise.
        """
    
        user = User.objects.get(id = request.auth.user_id) 
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(MedicalHistory)
        
        return group.permissions.filter(content_type=content_type, codename ='view_medicalhistory').exists()
        
    
    
class IsNurse(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and belongs to the 'Nurse' group.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and belongs to the 'Nurse' group.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and belongs to the 'Nurse' group.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and belongs to the 'Nurse' group,
                  False otherwise.
        """
        if request.user.groups.filter(name = "Nurse").exists() and request.user.is_nurse:
            return True
        
class IsAppointment(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and belongs to a group with the appropriate permissions for the requested HTTP method.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and belongs to a group
            with the appropriate permissions for the requested HTTP method.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and belongs to a group
        with the appropriate permissions for the requested HTTP method.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and belongs to a group
                  with the appropriate permissions for the requested HTTP method, False otherwise.
        """
        codenames = {
            'POST' : 'add_appointment',
            'GET' : 'view_appointment',
            'DELETE' : 'delete_appointment',
            'PATCH' : 'change_appointment'
        }
        
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Appointment)
        if user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        
        return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        
class IsOrder(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and has the appropriate permissions to view, add, change, or delete orders.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete orders.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete orders.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete orders, False otherwise.
        """

        codenames = {
            'POST' : 'add_order',
            'GET' : 'view_order',
            'DELETE' : 'delete_order',
            'PATCH' : 'change_order'
        }
        
        
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Order)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return [IsAuthenticated()]
    
class IsOrderDetail(IsAuthenticated):  
    """
    Permission class that allows access only if the requesting user is authenticated
    and has the appropriate permissions to view, add, change, or delete order details.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete order details.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete order details.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete order details, False otherwise.
        """
        codenames = {
            'POST' : 'add_orderdetail',
            'GET' : 'view_orderdetail',
            'DELETE' : 'delete_orderdetail',
            'PATCH' : 'change_orderdetail'
        }
         
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(OrderDetail)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return [IsAuthenticated()]
    
class IsSchedule(IsOrder):  
    """
    Permission class that allows access only if the requesting user is authenticated
    and has the appropriate permissions to view, add, change, or delete schedules.

    Extends:
        IsOrder

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete schedules.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete schedules.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete schedules, False otherwise.
        """
        codenames = {
            'POST' : 'add_schedule',
            'GET' : 'view_schedule',
            'DELETE' : 'delete_schedule',
            'PATCH' : 'change_schedule'
        }
         
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Schedule)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return [IsAuthenticated()]
    
class IsScheduleDetail(IsAuthenticated):  
    """
    Permission class that allows access only if the requesting user is authenticated and has
    the appropriate permissions to view, add, change, or delete schedule details.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete schedule details.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete schedule details.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete schedule details, False otherwise.
        """
        codenames = {
            'POST' : 'add_scheduledetail',
            'GET' : 'view_scheduledetail',
            'DELETE' : 'delete_scheduledetail',
            'PATCH' : 'change_scheduledetail'
        }
         
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(ScheduleDetail)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return [IsAuthenticated()]
    
class IsMedecine(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and has the appropriate permissions to view, add, change, or delete medicine.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete medicine.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete medicine.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete medicine, False otherwise.
        """
        codenames = {
            'POST' : 'add_medicine',
            'GET' : 'view_medicine',
            'DELETE' : 'delete_medicine',
            'PATCH' : 'change_medicine'
        }
         
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Medicine)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return False
    
class IsCategory(IsAuthenticated):
    """
    Permission class that allows access only if the requesting user is authenticated
    and has the appropriate permissions to view, add, change, or delete categories.

    Extends:
        IsAuthenticated

    Methods:
        has_permission(request, view):
            Check if the requesting user is authenticated and has the appropriate permissions
            to view, add, change, or delete categories.

    Attributes:
        None.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated and has the appropriate permissions
        to view, add, change, or delete categories.

        Args:
            request (HttpRequest): The HTTP request instance.
            view (django.views.View): The view instance.

        Returns:
            bool: True if the requesting user is authenticated and has the appropriate permissions
                  to view, add, change, or delete categories, False otherwise.
        """
        codenames = {
            'POST' : 'add_category',
            'GET' : 'view_category',
            'DELETE' : 'delete_category',
            'PATCH' : 'change_category'
        }
         
        user = User.objects.get(pk=request.auth.user_id)
        
        group = user.groups.first()
        
        content_type = ContentType.objects.get_for_model(Category)
        
        if user.is_staff:
            return [IsAdminUser()]
        elif user.is_nurse:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
        elif user.is_doctor:
            return group.permissions.filter(content_type=content_type, codename = codenames[request.method]).exists()
    
        return False