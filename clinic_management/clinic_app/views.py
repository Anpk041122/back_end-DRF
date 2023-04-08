from .serializers import CategorySerializer, MedicineSerializer, UserSerializer, MedicalHistorySerializer
from .models import Category, Medicine, User, MedicalHistory
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
                return [IsAdminUser]
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
        return Response(UserSerializer(request.user).data)

    
# search by user 
class MedicineViewSet(viewsets.ViewSet , generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def filter_queryset(self, queryset):
        kw = self.request.query_params.get('kw')
        if self.action.__eq__('list') and kw:
            queryset = queryset.filter(name__icontains=kw)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

# get all use by admin
class CategoryViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]       
    parser_classes = [MultiPartParser , ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

