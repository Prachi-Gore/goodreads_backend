from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserStatusViewSet,NotificationViewSet,GroupViewSet,MessageViewSet


router = DefaultRouter()
router.register(r'user-group', UserStatusViewSet, basename='user-group') # basename could be different
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register('group', GroupViewSet, basename='group')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('chat/', include(router.urls))
]         
