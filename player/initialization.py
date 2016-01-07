from django.apps import AppConfig
from django.conf import settings


class Init(AppConfig):
    name = 'player'
    verbose_name = 'Player'

    def ready(self):
        from player.models import Events
        if not settings.TESTING:
            Room = self.get_model('Room')
            # Initialize events dict and clean rooms
            try:
                for room in Room.objects.all():
                    Events.set(room, None)
                    room.current_music = None
                    room.shuffle = False
                    room.save()
            except Exception as e:
                print('Error during initilization: %s' % e)
