from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('category', views.CategoryViewSet)
router.register('medicine', views.MedicineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('patient/<int:id>/', views.PatientViewSet.as_view(), name="patient")
]