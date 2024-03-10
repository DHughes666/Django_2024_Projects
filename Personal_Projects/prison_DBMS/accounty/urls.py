from django.urls import path, include
from rest_framework import routers
from .views import InmateViewSet, StaffViewSet


router = routers.DefaultRouter()
router.register(r'inmates', InmateViewSet)
router.register(r'staff', StaffViewSet)

urlpatterns = [
    path('', include(router.urls)),
]