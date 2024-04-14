from django.urls import path
from .consumer import PersonalChatConsumer


websocket_urlpatterns = [
    path("ws/chat/<int:receiver_id>/", PersonalChatConsumer.as_asgi())
]