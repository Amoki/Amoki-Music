from django.apps import AppConfig
from django.conf import settings


class Init(AppConfig):
    name = 'music'
    verbose_name = 'Music'

    def ready(self):
        if not settings.TESTING:
            from .models import PlaylistTrack

            try:
                # Delete all playlists
                PlaylistTrack.objects.all().delete()
            except Exception as e:
                print('Error during initilization: %s' % e)
