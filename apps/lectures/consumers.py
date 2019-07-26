import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from lectures.models import Lecture


class LectureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lecture_token = self.scope['url_route']['kwargs']['token']
        user = self.scope['user']
        if (await self.check_lecture()) and user.is_staff:
            await self.channel_layer.group_add(
                self.lecture_token,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()
            await self.close(code=4123)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.lecture_token,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.lecture_token,
        #     {
        #         'type': 'lecture_notification',
        #         'message': message
        #     }
        # )

    async def lecture_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def check_lecture(self):
        return Lecture.objects.filter(link_token=self.lecture_token).exists()
