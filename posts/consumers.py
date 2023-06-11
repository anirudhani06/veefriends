from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.activity_room = self.scope["url_route"]["kwargs"]["username"]
        await self.channel_layer.group_add(self.activity_room, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.activity_room, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_activity(self, event):
        user = event["user"]
        user_img = event["user_img"]
        message = event["message"]
        post = event["post"]

        await self.send(
            text_data=json.dumps(
                {
                    "user": user,
                    "message": message,
                    "user_img": user_img,
                    "post": post,
                }
            )
        )
