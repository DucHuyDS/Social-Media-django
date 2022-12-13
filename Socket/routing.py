from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/<int:room_id>/',consumers.ChatConsumer.as_asgi()),
    path('ws/notifications/<int:user_id>/',consumers.Notifications.as_asgi()),
]