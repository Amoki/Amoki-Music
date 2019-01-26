from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive_json(self, content):
        message = content["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "room_message", "message": message}
        )

    # Receive message from room group
    def room_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send_json(content={"message": message})
