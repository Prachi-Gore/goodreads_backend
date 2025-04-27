from rest_framework import viewsets, permissions,status
from django.contrib.auth import get_user_model
from .serializers import UserStatusSerializer,NotificationSerializer,GroupSerializer
from .models import Notification,ConnectionRequest,Group
from rest_framework.response import Response
from .utils import save_and_send_real_time_notification
from django.db.models import Q
from rest_framework.decorators import action

User = get_user_model()

class UserStatusViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    serializer_class = UserStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude( Q(id=self.request.user.id) | Q(is_superuser=True)) # except login user
    
    def create(self, request, *args, **kwargs):
        """
        POST /chat/user-status/
        Payload: { "receiver_id": 2 }
        Purpose: Send a connetion request
        """
        print("create create trigger")
        sender = request.user
        receiver_id = request.data.get("receiver_id")

        if not receiver_id:
            return Response({"error": "Receiver ID required."}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)

            if ConnectionRequest.objects.filter(sender=sender, receiver=receiver).exists():
                return Response({"error": "Request already sent."}, status=400)

            ConnectionRequest.objects.create(sender=sender, receiver=receiver)
   
            msg=f"{sender.username} sent you a connetion request."
            print("before create trigger")
            save_and_send_real_time_notification(receiver,msg)
            print("after create trigger")


            return Response({"success": "connection request sent."}, status=201)

        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=404)

    # detail=False it means while update we are not passing any id in url
    @action(detail=False, methods=['put'], url_path='update')
    def update_user_status(self, request):
        """
        PUT /chat/user-status/
        Payload: { "sender_id": 3, "status": "accepted" | "rejected" }
        Purpose: Accept or reject a connetion request
        """
        receiver = request.user
        sender_id = request.data.get("sender_id")
        new_status = request.data.get("status")

        if not sender_id or new_status not in ["accepted", "rejected"]:
            return Response({"error": "Sender ID and valid status required."}, status=400)

        try:
            sender = User.objects.get(id=sender_id)
            connection = ConnectionRequest.objects.get(sender=sender, receiver=receiver, status='pending')

            connection.status = new_status
            connection.save()
            msg=f"{receiver.username} {new_status} your connetion request."
            save_and_send_real_time_notification(sender,msg)
            return Response({"success": f"connetion request {new_status}."})

        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=404)
        except ConnectionRequest.DoesNotExist:
            return Response({"error": "No pending request from this user."}, status=404)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at') # latest should be on top

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        notifications = self.get_queryset().filter(is_read=False)
        updated_count = notifications.update(is_read=True)
        return Response({
            "message": f"{updated_count} notifications marked as read."
        }, status=status.HTTP_200_OK)
    
    # def perform_update(self, serializer):
    #     # Optional: Ensure only the owner can update their own notifications
    #     serializer.save(recipient=self.request.user)

    # def perform_destroy(self, instance):
    #     # Optional: Ensure only the owner can delete their own notifications
    #     if instance.recipient == self.request.user:
    #         instance.delete()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return self.request.user.groups.all()