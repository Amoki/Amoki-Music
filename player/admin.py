from django.contrib import admin
from player.models import Music
from player.helpers import get_youtube_link


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'url', 'duration', 'date', 'last_play')

    def url(self, music):
        return get_youtube_link(music.video_id)

    def has_add_permission(self, request):
        return False

admin.site.register(Music, MusicAdmin)
