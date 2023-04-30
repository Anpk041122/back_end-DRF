from .serializers import ( 
    CategorySerializer, MedicineSerializer, 
    UserSerializer, MedicalHistorySerializer, 
    PatientSerializer, EmployeeSerializer,
    MedicalHistory, AdminUserSerializer, AppointmentSerializer,
    ScheduleSerializer, ScheduleDetailSerializer, OrderDetailSerializer,
    OrderSerializer,
    )
from .models import ( 
    Category, Medicine, User, 
    MedicalHistory, Patient,
    Employee, Appointment, Schedule,
    ScheduleDetail, Order, OrderDetail,
    
    
)
from rest_framework import ( 
    viewsets, generics, filters
    )
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAuthenticated, IsAdminUser
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from . import perms
from django.contrib.auth.hashers import make_password
from .paginators import MedicinePaginator
# User : manage account of empolyee and paitent
class UserViewSet(viewsets.ViewSet, generics.RetrieveUpdateDestroyAPIView, generics.ListCreateAPIView):
    """
    Viewset for User model.

    Args:
        viewsets (type): A viewset class from Django REST Framework.
        generics (type): Generic views to provide CRUD functionality.

    Returns:
        Response: A response object.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        """
        Get the permissions that the current request has.

        Returns:
            List: A list of permission classes.
        """
        if self.action in [ 'update', 'retrieve', 'partial_update']:
            if self.request.user.is_staff:
                return [IsAdminUser()]
            return [perms.IsPatientUser(), perms.IsSelf()]
        
        if self.action in ['list', 'destroy']:    
            return [IsAdminUser()]

        return [AllowAny()]
    
    def update(self, request, *args, **kwargs):
        """
        Update the user instance.

        Args:
            request (HttpRequest): The request instance.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response object.
        """
        u = self.get_object()
        serializer = self.get_serializer(u, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username = u)
        user.set_password(request.data['password'])
        user.save()
        return Response(serializer.data)

    
    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        """
        Get the current user instance.

        Args:
            request (HttpRequest): The request instance.

        Returns:
            Response: A response object.
        """
        print(request.user)
        return Response(UserSerializer(request.user).data)

class AdminUserViewSet(generics.CreateAPIView, viewsets.ViewSet):
    """
    Viewset for creating admin users.

    Extends:
        generics.CreateAPIView

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = AdminUserSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Viewset for creating admin users.

        Extends:
            generics.CreateAPIView

        Methods:
            get_permissions():
                Returns the permission classes that this view requires.

        Attributes:
            queryset (QuerySet): The default queryset for this viewset.
            serializer_class (Serializer): The serializer class for this viewset.
            parser_classes (list): The parser classes that this view can handle.
            renderer_classes (list): The renderer classes that this view can use.
        """
        if self.request.method == "POST":
            return [IsAdminUser()]
    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        """
        Get the current user instance.

        Args:
            request (HttpRequest): The request instance.

        Returns:
            Response: A response object.
        """
        print(request.user)
        return Response(UserSerializer(request.user).data)
        
class PatientViewSet(generics.RetrieveUpdateAPIView, generics.ListAPIView):
    """
    A viewset that provides GET and PUT methods for retrieving and updating patient records,
    and GET method for listing patient records.

    Extends:
        generics.RetrieveUpdateAPIView
        generics.ListAPIView

    Methods:
        get_permissions():
            Returns the permission classes that should be applied to the viewset.

    Attributes:
        queryset (QuerySet): The queryset to use for retrieving patient records.
        serializer_class (PatientSerializer): The serializer class to use for serializing patient records.
        parser_classes (list of Parser classes): The list of parser classes to use for parsing request payloads.
        renderer_classes (list of Renderer classes): The list of renderer classes to use for rendering response payloads.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that should be applied to the viewset based on the request method.

        Returns:
            list of Permission classes: The list of permission classes to apply.
        """
        if self.request.method in [ 'retrieve', 'update']:
            if self.request.user.is_staff:
                return [IsAdminUser(), IsAuthenticated()]
            else:
                return [perms.IsCustomerPatient()]
        else:
            return [IsAdminUser()]
    
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Employee instances.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.

        If the requested action is 'list', requires that the user is an Employee.
        Otherwise, requires that the user is an Admin.

        Returns:
            list: A list of permission classes.
        """
        if self.action in [ 'list']:
            return [perms.IsEmployee()]
        return [IsAdminUser()]
    

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for creating, retrieving, updating and deleting medical histories.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.
        get_queryset():
            Returns the queryset for this viewset based on the request parameters.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.

        Returns:
            list: A list of permission classes for this viewset.
        """
        if self.action in ['retrieve','list']:
                return [perms.IsDoctorMedicalHistory()]
            
        return [IsAdminUser()]
        
    def get_queryset(self):
        """
        Returns the queryset for this viewset based on the request parameters.

        Returns:
            QuerySet: The filtered queryset for this viewset.
        """
        queryset = self.queryset

        # Get the patient name or ID value from query params
        patient_name = self.request.query_params.get('patient_name', None)
        patient_id = self.request.query_params.get('patient_id', None)

        if patient_name:
            # Filter MedicalHistory by patient name
            queryset = queryset.filter(patient__name__icontains=patient_name)

        if patient_id:
            # Filter MedicalHistory by patient ID
            queryset = queryset.filter(patient_id=patient_id)

        return queryset
    
class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing appointments.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.
        get_queryset():
            Returns the queryset for this view based on the request parameters.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        """
        Returns the permission classes that this view requires.

        Nurses can view and manage appointments. Patients can only view their own appointments.

        Returns:
            list: A list of permission classes.
        """
        user = User.objects.get(id=self.request.auth.user_id)
        if user.is_nurse:
            return [perms.IsAppointment()]
        else:
            return [perms.IsAppointment(), perms.IsSelf()]

    def get_queryset(self):
        """
        Returns the queryset for this view based on the request parameters.

        If a patient ID is specified in the query parameters, return only the appointments for that patient.

        Returns:
            QuerySet: The queryset for this view.
        """
        queryset = self.queryset

        patient_id = self.request.query_params.get('patient_id', None)

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing orders.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.
        
        Permissions:
            IsOrder: Allows access to authenticated users who have the 'order' permission.
        """
        return [perms.IsOrder()]
    

class OrderDetailViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing order details.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.
        
        Permissions:
            IsOrderDetail: Allows access to authenticated users who have the 'orderdetail' permission.
        """
        return [perms.IsOrderDetail()]
    
class ScheduleViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing schedules.

    Extends:
        viewsets.ModelViewSet

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.

        Permissions:
            Schedule: Allows access to authenticated users who have the 'Schedule' permission.
        """
        return [perms.IsSchedule()]
    
class ScheduleDetailViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing schedule details.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        parser_classes (list): The parser classes that this view can handle.
        renderer_classes (list): The renderer classes that this view can use.

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.
    """
    queryset = ScheduleDetail.objects.all()
    serializer_class = ScheduleDetailSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.
        
        Permissions:
            ScheduleDetail: Allows access to authenticated users who have the 'ScheduleDetail' permission.
        """
        return [perms.IsScheduleDetail()]
    
# search by user 
class MedicineViewSet(viewsets.ViewSet , viewsets.ModelViewSet):
    """
    Viewset for retrieving and filtering medicines.

    Extends:
        viewsets.ViewSet
        generics.ListAPIView

    Methods:
        get_permissions():
            Returns the permission classes that this view requires.
        filter_queryset(queryset):
            Filters the queryset based on the query parameters.

    Attributes:
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
        filter_backends (list): The filter backends to use for this viewset.
        search_fields (list): The fields to search against using the SearchFilter.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    pagination_class = MedicinePaginator
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_permissions(self):
        """
        Returns the permission classes that this view requires.
        
        Permissions:
            Medicine: Allows access to authenticated users who have the 'Medicine' permission.
        """
        return [perms.IsMedecine()]
    
    def filter_queryset(self, queryset):
        """
        Filters the queryset based on the query parameters.

        Args:
            queryset (QuerySet): The queryset to filter.

        Returns:
            The filtered queryset.
        """
        kw = self.request.query_params.get('kw')
        if self.action.__eq__('list') and kw:
            queryset = queryset.filter(name__icontains=kw)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset


# get all use by admin
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing categories.

    Extends:
        viewsets.ModelViewSet

    Methods:
        get_permissions():
        Returns the permission classes that this view requires.

    Attributes:
        renderer_classes (list): The renderer classes for this viewset.
        parser_classes (list): The parser classes for this viewset.
        queryset (QuerySet): The default queryset for this viewset.
        serializer_class (Serializer): The serializer class for this viewset.
    """ 
    renderer_classes = [JSONRenderer]       
    parser_classes = [MultiPartParser , ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Returns the permission classes that this view requires.
        
        Permissions:
            Category: Allows access to authenticated users who have the 'Category' permission.
        """
        return [perms.IsCategory()]
