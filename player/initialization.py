from django.apps import AppConfig
from player.models import events
from django.conf import settings


class Init(AppConfig):
    name = 'player'
    verbose_name = 'Player'

    def ready(self):
        if not settings.TESTING:
            Room = self.get_model('Room')
            try:
                for room in Room.objects.all():
                    events[room.name] = None
                    room.current_music = None
                    room.shuffle = False
                    room.save()
            except Exception as e:
                print ('Error during initilization: %s' % e)
