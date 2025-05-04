from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def save_and_send_real_time_notification(recipient,msg,isNotification,type):
     # Save to Notification table
     if(isNotification):
        Notification.objects.create(
                recipient=recipient,
                message=msg
            )
     # Trigger WebSocket
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
                f"user_{recipient.id}",
                {
                    "type": type, # this method has implemented inside consumer and this object will become our event
                    "message": msg
                }
            )
     print("WebSocket trigger",recipient.id,type)