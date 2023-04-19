from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('category', views.CategoryViewSet)
router.register('medicine', views.MedicineViewSet)
router.register('employee', views.EmployeeViewSet)
router.register('medical_history', views.MedicalHistoryViewSet)
router.register('appointment', views.AppointmentViewSet)
router.register('order', views.OrderViewSet)
router.register('order_detail', views.OrderDetailViewSet)
router.register('schedule', views.ScheduleViewSet)
router.register('schedule_detail', views.ScheduleDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('patient/<int:id>/', views.PatientViewSet.as_view(), name="patient"),
    path('admin_employee/', views.AdminUserViewSet.as_view(), name="admin_employee"),
]