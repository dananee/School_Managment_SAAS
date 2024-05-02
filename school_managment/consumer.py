import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from school_managment.serialization import NotificationSerializer
from .models import Notification
from .models import SchoolMembers
import datetime


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.role = self.scope["url_route"]["kwargs"]["role"]
        self.group_name = f"role_{self.role}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            "type": "send_message",
            "message": message,
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):

        data = event["message"]
        await self.create_message(data=data)

        response_data = {
            "author": data["author"],
            "status": data["status"],
            "role": data["role"],
            "sender": data["sender_id"],
            "message": data["message"],
        }

        await self.send(text_data=json.dumps(response_data))

    @database_sync_to_async
    def create_message(self, data):
        role = data["role"]
        get_member_by_role = SchoolMembers.objects.filter(role=role)

        if not Notification.objects.filter(message=data["message"]).exists():
            new_message = NotificationSerializer(data=data)
            if new_message.is_valid():
                new_message.save()
            else:
                ValueError(f"Notification error : {new_message.error_messages}")

    @database_sync_to_async
    def get_unread_notifications(self, role):
        unread_notifications = Notification.objects.filter(role=role, read=False)
        return [
            {"message": notification.message, "timestamp": notification.timestamp}
            for notification in unread_notifications
        ]
