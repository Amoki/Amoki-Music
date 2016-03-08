# -*- coding: utf-8 -*-
from django.conf import settings
from ws4redis.subscriber import RedisSubscriber
from player.models import Room
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json
from django.core.exceptions import PermissionDenied


class CustomSubscriber(RedisSubscriber):
    """
    Subscriber class, used by the websocket code to listen for subscribed channels
    """
    subscription_channels = ['subscribe-session', 'subscribe-group', 'subscribe-user', 'subscribe-broadcast']
    publish_channels = ['publish-session', 'publish-group', 'publish-user', 'publish-broadcast']

    def __init__(self, connection):
        self.request = None
        super(CustomSubscriber, self).__init__(connection)

    def set_pubsub_channels(self, request, channels):
        """
        Initialize the channels used for publishing and subscribing messages through the message queue.
        """
        super(CustomSubscriber, self).set_pubsub_channels(request, channels)

        self.request = request
        self.update_room_listeners(self.request)

    def release(self):
        """
        New implementation to free up Redis subscriptions when websockets close. This prevents
        memory sap when Redis Output Buffer and Output Lists build when websockets are abandoned.
        """
        super(CustomSubscriber, self).release()
        self.update_room_listeners(self.request)

    def update_room_listeners(self, request):
        facility = request.path_info.replace(settings.WEBSOCKET_URL, '', 1)

        if facility not in [room.token for room in Room.objects.all()]:
            raise PermissionDenied("Unknow room")

        prefix = self.get_prefix()
        key = prefix + 'broadcast:' + facility
        query = self._connection.execute_command('PUBSUB', 'NUMSUB', key)

        room_to_update = Room.objects.get(token=facility)
        room_to_update.listeners = query[1] if len(query) > 1 else 0
        room_to_update.save()

        redis_publisher = RedisPublisher(facility=room_to_update.token, broadcast=True)
        message = {
            'action': 'listeners_updated',
            'listeners': room_to_update.listeners
        }
        listenersMessage = RedisMessage(json.dumps(message))
        redis_publisher.publish_message(listenersMessage)
