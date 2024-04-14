from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import User, ChatMessage
from .serializer import MessageSerializer
from .utils import LOGGER, get_user
from channels.db import database_sync_to_async


class PersonalChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer for personal chat between two users.
    """

    async def connect(self):
        # Check if user is authenticated
        if self.scope["user"].is_authenticated:
            # Get ids of users who chat with each other and sort them
            self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
            user_ids = sorted([self.scope["user"].id, self.receiver_id])
            # Create a group name for this chat
            self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # Reject the connection if user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Get the receiver of this message
        receiver = await get_user(self.receiver_id)

        # Save the message to DB
        try:
            chat_obj = await self.save_message_to_db(self.scope["user"], receiver, text_data)
        except Exception as e:
            LOGGER.warning(f"Error saving message {e}")

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_obj
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_message_to_db(self, user, receiver, message):
        """
        Save a message to DB.
        """
        chat_obj = ChatMessage.objects.create(user=user, sender=user, receiver=receiver, message=message)
        chat_obj.save()
        return MessageSerializer(chat_obj).data


