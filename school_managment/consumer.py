from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async

from school_managment.models import NotificationModel, SchoolMembers
from school_managment.serialization import NotificationSerializer



class NotificationConsumer(AsyncJsonWebsocketConsumer):
    

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('notification', self.channel_name)
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification",self.channel_name)

    async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json
    
            event = {
                'type': 'send_message',
                'message': message,
            }
    
            await self.channel_layer.group_send("notification",event)
     

    async def send_message(self, event):
    
            data = event['message']
            await self.create_message(data=data)
    
            response_data = {
                'sender':data["sender"],
                'message': data['message']
            }

             
            await self.send(text_data=json.dumps( response_data ))   
        
    
    @database_sync_to_async
    def create_message(self, data):

         
        get_sender_by_id = SchoolMembers.objects.get(id=data['sender'])
        if not NotificationModel.objects.filter(message=data['message']).exists():
            new_message = NotificationSerializer(  sender=get_sender_by_id, message=data['message'])
            new_message.save()