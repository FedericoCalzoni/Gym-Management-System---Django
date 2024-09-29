import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'noti_group_name'
       
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    
    def receive(self,text_data):
        # This method is for handling messages sent from the client, if needed.
        pass

    def disconnect(self,close_code):
        self.close(close_code)

    def send_notification(self,event):
        data = json.loads(event['value'])
        
        self.send(text_data=json.dumps({
            'notif_id': data.get('notif_id'),
            'notif': data.get('notif'),
            'total': data.get('total'),
            'action': data.get('action')  # 'add' or 'delete'
        }))


# class TrainerChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.subscriber_id = self.scope['url_route']['kwargs']['subscriber_id']
#         self.group_name = f'chat_{self.subscriber_id}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json['sender']

#         # Send message to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'sender': sender,
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }))


# class SubscriberChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Use the room name passed in the URL (unique for each subscriber)
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         await self.channel_layer.group_add(self.room_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender = data['sender']
        
#         # Broadcast the message to the group (room)
#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }))

class TrainerChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.subscriber_id = self.scope['url_route']['kwargs']['subscriber_id']
        self.group_name = f'chat_{self.subscriber_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))


class SubscriberChatConsumer(AsyncWebsocketConsumer):
   
    async def connect(self):
        self.subscriber_id = self.scope['url_route']['kwargs']['subscriber_id'] 
        self.group_name = f'chat_{self.subscriber_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
