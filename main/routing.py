from django.urls import path,re_path
from .consumers import NotificationsConsumer,TrainerChatConsumer,SubscriberChatConsumer

ws_patterns = [
    path('ws/notifications/',NotificationsConsumer.as_asgi()),
    path('ws/Trainer-Chat/<int:subscriber_id>/',TrainerChatConsumer.as_asgi(),name="ws_trainer_chat"),
    path('ws/Subscriber-Chat/<int:subscriber_id>/', SubscriberChatConsumer.as_asgi()),
]