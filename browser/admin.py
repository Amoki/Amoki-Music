from django.contrib import admin
from browser.models import Music
from browser.helpers import get_youtube_link


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'url', 'date')

    def url(self, music):
        return get_youtube_link(music.video_id)

admin.site.register(Music, MusicAdmin)
