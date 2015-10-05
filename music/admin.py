from django.contrib import admin
from music.models import Music

from music.serializers import MusicSerializer


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'music_id', 'source', 'duration', 'last_play', 'dead_link', 'thumbnail', 'room', 'timer_start', 'timer_end')
    actions = ('add_music',)

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            # Hack to transform music into dict
            music.room.add_music(**MusicSerializer(music).data)
        return

admin.site.register(Music, MusicAdmin)
