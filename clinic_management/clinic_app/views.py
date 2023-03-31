from django.shortcuts import render
from django.http import HttpResponse
from .views.CategoryView import CategoryView 
from .serializers import CategorySerializer, MedicineSerializer, UserSerializer
from .models import Category, Medicine, User
from rest_framework import ( 
    viewsets, generics, filters, status
    )
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAuthenticated, IsAdminUser
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# User : manage account of empolyee and paitent
class UserViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        if self.action in ['current_user', 'update', 'partial_update']:
            return [IsAuthenticated()]

        # if self.action in ['admin_create_user']:
        #     return [IsAdminUser()]
        
        return [AllowAny()]


    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
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
    parser_classes = [MultiPartParser, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#test git
