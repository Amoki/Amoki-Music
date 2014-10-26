from django.apps import AppConfig
from player.models import events
from django.contrib.sessions.models import Session


class Init(AppConfig):
    name = 'player'
    verbose_name = 'Player'

    def ready(self):
        Session.objects.all().delete()
        Room = self.get_model('Room')
        for room in Room.objects.all():
            events[room.name] = None
            room.current_music = None
            room.suffle = False
            room.save()
