# chat/consumers.py
import json

from rest_framework import serializers

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import channels.layers

from thu_lost_and_found_backend.user_service.models import User
from .models import Message


# TODO: periodically remove sent message to avoid overwhelming storage.
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = eval(self.scope['url_route']['kwargs']['user'])
        try:
            user = User.objects.get(pk=self.user)
        except User.DoesNotExist:
            return

        user.channel_name = self.channel_name
        user.save()

        self.accept()

        unsent_messages = Message.objects.filter(receiver=user, sent=False)
        for unsent_message in unsent_messages:
            unsent_message.sent = True
            unsent_message.save()
            self.send(text_data=json.dumps({
                'message': unsent_message.message,
                'sender': unsent_message.sender.id,
                'time': serializers.DateTimeField().to_representation(unsent_message.time)
            }))

    def disconnect(self, close_code):
        try:
            user = User.objects.get(pk=self.user)
        except User.DoesNotExist:
            return

        user.channel_name = None
        user.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = self.user
        receiver_id = int(text_data_json['receiver'])
        message = text_data_json['message']
        self.send_message(sender_id, receiver_id, message)

    def send_message(self, sender_id, receiver_id, message):
        try:
            sender = User.objects.get(pk=sender_id)
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return

        message_obj = Message.objects.create(sender=sender, receiver=receiver, message=message)

        if receiver.channel_name:
            message_obj.sent = True
            if not hasattr(self, "channel_layer"):
                self.channel_layer = channels.layers.get_channel_layer()

            async_to_sync(self.channel_layer.send)(
                receiver.channel_name,
                {
                    'type': 'chat.message',
                    'sender': sender_id,
                    'message': message,
                    'time': serializers.DateTimeField().to_representation(message_obj.time)
                }
            )

        message_obj.save()

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'time': event['time']
        }))