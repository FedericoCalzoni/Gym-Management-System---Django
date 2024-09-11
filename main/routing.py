from django.urls import path
from .consumers import NotificationsConsumer

ws_patterns = [
    path('ws/notifications/',NotificationsConsumer.as_asgi())
]