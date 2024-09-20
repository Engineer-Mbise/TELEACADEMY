# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from courses.models import Course  # Assuming Course model is in courses app
from .models import Message
from authentication.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"course_{self.scope['url_route']['kwargs']['pk']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close(code)
        
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        event = {
            "type": "send_message",
            "message": data_json,  
        }
        await self.channel_layer.group_send(self.room_name, event)
        
    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response = {
            "sender": data['sender'],
            "message": data["message"],
        }
        await self.send(text_data=json.dumps({"message": response}))
    
    @database_sync_to_async
    def create_message(self, data):
        course_id = self.scope['url_route']['kwargs']['pk']
        course = Course.objects.get(id=course_id)
        user = User.objects.get(email=data['sender'])  # Assuming 'sender' is an email
        # if not Message.objects.filter(message=data['message'], sender=user, course=course).exists():
        message = Message.objects.create(
            message=data['message'],
            sender=user,
            course=course
        )
   

