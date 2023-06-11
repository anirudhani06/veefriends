from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from accounts.models import Profile
from .models import ChatRoom, ChatRoomMessage, Chat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"]
        self.receiver = self.scope["url_route"]["kwargs"]["username"]

        self.chat_name = await self.get_chat()

        await self.channel_layer.group_add(self.chat_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]

        await self.save_chat(message)

        await self.channel_layer.group_send(
            self.chat_name,
            {"type": "send_message", "message": message, "user": self.sender},
        )

    async def send_message(self, event):
        user = event["user"].username
        url = await self.get_user_url(user)
        message = event["message"]

        await self.send(
            text_data=json.dumps({"user": user, "url": url, "message": message})
        )

    @database_sync_to_async
    def get_user_url(self, username):
        user = Profile.objects.filter(username=username).first()
        return user.get_absolute_url

    @database_sync_to_async
    def get_chat(self):
        sender = Profile.objects.filter(username=self.sender).first()
        receiver = Profile.objects.filter(username=self.receiver).first()
        room = f"chat-{sender.id}-{receiver.id}"
        chat_thread = Chat.objects.filter(room=room).first()

        if chat_thread == None:
            chat_thread, _ = Chat.objects.get_or_create(
                room=f"chat-{receiver.id}-{sender.id}"
            )

        return chat_thread.room

    @database_sync_to_async
    def save_chat(self, message):
        user = Profile.objects.filter(username=self.sender).first()
        chat = Chat.objects.filter(room=self.chat_name).first()
        chat_msg = ChatMessage()
        chat_msg.chat = chat
        chat_msg.user = user
        chat_msg.message = message
        chat_msg.save()


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room"]
        self.chat_room_name = self.room_name.replace(" ", "_")
        await self.channel_layer.group_add(self.chat_room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.chat_room_name,
            {"type": "send_message", "user": self.user, "message": message},
        )

    async def send_message(self, event):
        message = event["message"]
        user = event["user"].username

        await self.send(text_data=json.dumps({"message": message, "user": user}))

    @database_sync_to_async
    def save_message(self, message):
        user = Profile.objects.get(username=self.user)
        chat_room = ChatRoom.objects.filter(room=self.room_name).first()

        chat_messages = ChatRoomMessage()
        chat_messages.room = chat_room
        chat_messages.user = user
        chat_messages.message = message

        chat_messages.save()
