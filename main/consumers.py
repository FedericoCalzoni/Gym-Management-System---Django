import json
from channels.generic.websocket import WebsocketConsumer
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

 