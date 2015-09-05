from django.apps import AppConfig


class Init(AppConfig):
    name = 'music'
    verbose_name = 'Music'

    def ready(self):
        PlaylistTrack = self.get_model('PlaylistTrack')
        try:
            PlaylistTrack.objects.all().delete()
        except Exception, e:
            print ('Error during initilization: %s' % e)
