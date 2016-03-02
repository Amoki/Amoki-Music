# -*- coding: utf-8 -*-
from django.conf import settings
from ws4redis.redis_store import SELF
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
        self._subscription = None
        self.request = None
        super(CustomSubscriber, self).__init__(connection)

    def set_pubsub_channels(self, request, channels):
        """
        Initialize the channels used for publishing and subscribing messages through the message queue.
        """
        facility = request.path_info.replace(settings.WEBSOCKET_URL, '', 1)

        # initialize publishers
        audience = {
            'users': 'publish-user' in channels and [SELF] or [],
            'groups': 'publish-group' in channels and [SELF] or [],
            'sessions': 'publish-session' in channels and [SELF] or [],
            'broadcast': 'publish-broadcast' in channels,
        }
        self._publishers = set()
        for key in self._get_message_channels(request=request, facility=facility, **audience):
            self._publishers.add(key)

        # initialize subscribers
        audience = {
            'users': 'subscribe-user' in channels and [SELF] or [],
            'groups': 'subscribe-group' in channels and [SELF] or [],
            'sessions': 'subscribe-session' in channels and [SELF] or [],
            'broadcast': 'subscribe-broadcast' in channels,
        }
        self._subscription = self._connection.pubsub()
        for key in self._get_message_channels(request=request, facility=facility, **audience):
            self._subscription.subscribe(key)

        self.request = request
        self.update_room_listeners(self.request)

    def release(self):
        """
        New implementation to free up Redis subscriptions when websockets close. This prevents
        memory sap when Redis Output Buffer and Output Lists build when websockets are abandoned.
        """

        if self._subscription and self._subscription.subscribed:
            self._subscription.unsubscribe()
            self._subscription.reset()
        self.update_room_listeners(self.request)

    def update_room_listeners(self, request):
        facility = request.path_info.replace(settings.WEBSOCKET_URL, '', 1)
        tokens = []
        for room in Room.objects.all():
            tokens.append(room.token)

        if facility not in tokens:
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
