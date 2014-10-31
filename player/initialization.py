from django.apps import AppConfig
from player.models import events


class Init(AppConfig):
    name = 'player'
    verbose_name = 'Player'

    def ready(self):
        Room = self.get_model('Room')
        try:
            for room in Room.objects.all():
                events[room.name] = None
                room.current_music = None
                room.shuffle = False
                room.save()
        except:
            print 'Error during initilization'
