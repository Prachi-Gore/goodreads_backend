from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserStatusViewSet,NotificationViewSet,GroupViewSet


router = DefaultRouter()
router.register(r'user-status', UserStatusViewSet, basename='user-status')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register('group', GroupViewSet, basename='group')

urlpatterns = [
    path('chat/', include(router.urls))
]         
