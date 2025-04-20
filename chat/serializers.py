from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ConnectionRequest,Notification
from custom_authentication.serializers import UserSerializer

User=get_user_model()

class UserStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    # user = UserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'status']

    def get_status(self, obj):
        current_user = self.context['request'].user

        # Case 1: Current user sent a request
        cr = ConnectionRequest.objects.filter(sender=current_user, receiver=obj).first()
        if cr:
            if cr.status == 'pending':
                return 'Pending'
            elif cr.status == 'accepted':
                return 'Friends'

        # Case 2: Other user sent a request to current user
        cr = ConnectionRequest.objects.filter(sender=obj, receiver=current_user).first()
        if cr:
            if cr.status == 'pending':
                return 'Accept_Reject'
            elif cr.status == 'accepted':
                return 'Friends'

        # No request found
        return 'Add_Friend'
    

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']