from django.apps import AppConfig
from django.conf import settings


class MusicConfig(AppConfig):
    name = "music"

    def ready(self):
        import music.signals

        if not settings.TESTING:
            from music.models import Room, Events, MusicQueue

            # Initialize events dict and clean rooms
            try:
                for room in Room.objects.all():
                    Events.set(room, None)
                    MusicQueue.objects.filter(room=room).delete()
                    room.shuffle = False
                    room.save()
            except Exception as e:
                print("Error during initilization: %s" % e)
