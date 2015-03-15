from django.contrib import admin
from music.models import Music


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'music_id', 'duration', 'date', 'last_play', 'dead_link', 'thumbnail', 'room', 'timer_start', 'timer_end')
    actions = ('add_music',)

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            music.room.push(music.url)
        return

admin.site.register(Music, MusicAdmin)
