<<<<<<< Updated upstream
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index")
=======
from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet)
router.register('medicines', views.MedicineViewSet)

urlpatterns = [
    path('', include(router.urls))
>>>>>>> Stashed changes
]