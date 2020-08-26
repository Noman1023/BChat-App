import json

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import asyncio

from chat.models import Channel, Thread, User, Message


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        # when the socket connects
        # self.kwargs.get("username")
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.send({
                "type": "websocket.accept"
            })
        else:
            await self.send({
                "type": "websocket.close"
            })
        print(self.user)
        thread_obj = await self.get_thread(self.user, self.other_username)
        self.chat_thread = thread_obj
        self.room_group_name = thread_obj.room_group_name  # group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.rando_user = await self.get_name()


        await self.create_channel()
        await self.set_online_status(self.user, True)

    async def websocket_receive(self, event):  # websocket.receive
        message_data = json.loads(event['text'])
        message = message_data['message']
        # user = await self.get_user(self.other_username)
        await self.create_message(self.chat_thread, self.user, message)
        print(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(message_data)
            }
        )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        await self.delete_channel()
        await self.set_online_status(self.user, False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_user(self, name):
        return User.objects.get(username=name)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_message(self, thread, sender, message):
        Message.objects.create(thread=thread, sender=sender, message=message)

    @database_sync_to_async
    def create_channel(self):
        Channel.objects.filter(user=self.user).delete()
        Channel.objects.create(channel_id=self.channel_name,
                               user=self.user,
                               thread=self.chat_thread,
                               )

    @database_sync_to_async
    def delete_channel(self):
        deleted = 0
        try:
            deleted, _ = Channel.objects.filter(channel_id=self.channel_name, user=self.user).delete()
            return deleted
        except:
            return deleted

    @database_sync_to_async
    def set_online_status(self, user, value):
        user.is_online = value
        user.save()