from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserStatusViewSet,NotificationViewSet
from django.urls import re_path
from . import consumers

router = DefaultRouter()
router.register(r'user-status', UserStatusViewSet, basename='user-status')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('chat/', include(router.urls))
]