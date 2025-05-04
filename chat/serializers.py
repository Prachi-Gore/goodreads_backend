# from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ConnectionRequest,Notification,Group,Message
from .utils import save_and_send_real_time_notification
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

class GroupSerializer(serializers.ModelSerializer):
    member_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = Group
        fields = ['id','name', 'member_ids']

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids')
        request_user = self.context['request'].user

        group = Group.objects.create(name=validated_data['name'], created_by=request_user)
        group.admins.add(request_user)
        group.members.add(*member_ids, request_user)  # add creator too

        # Create notifications
        User = get_user_model()
        members = User.objects.filter(id__in=member_ids)
        msg=f"{request_user.username} added you to group '{group.name}'"
        for member in members:
            # Send WebSocket notification 
            save_and_send_real_time_notification(recipient=member, msg=msg,isNotification=True,type="group_create")

        return group  

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'sender', 'created_at']      