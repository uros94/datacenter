from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import urlpatterns

from .views import DeviceViewSet, RackViewSet, DeviceAssignmentViewSet

router = DefaultRouter()
router.register('devices', DeviceViewSet, basename='device')
router.register('racks', RackViewSet, basename='rack')
router.register('assignments', DeviceAssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls))
]
