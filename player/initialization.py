from django.apps import AppConfig
from django.conf import settings


class Init(AppConfig):
    name = 'player'
    verbose_name = 'Player'

    def ready(self):
        if not settings.TESTING:
            from .models import Room, Events

            # Initialize events dict and clean rooms
            try:
                for room in Room.objects.all():
                    Events.set(room, None)
                    room.current_music = None
                    room.shuffle = False
                    room.save()
            except Exception as e:
                print('Error during initilization: %s' % e)
