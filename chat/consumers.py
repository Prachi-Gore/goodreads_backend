# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print("WebSocket connect", user.id)
        if user.is_authenticated:
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # You can ignore this if you're only sending from backend to frontend
        pass

    async def user_status(self, event):
        print("user_status hit")
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            # 'timestamp': event.get('timestamp')  
        }))

