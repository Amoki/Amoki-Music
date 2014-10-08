# -*- coding: utf-8 -*-

from django.contrib import admin
from player.models import Music, Player
from player.helpers import get_youtube_link


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'url', 'duration', 'date', 'last_play')
    actions = ('add_music',)

    def url(self, music):
        return get_youtube_link(music.video_id)

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            Player.push(music.video_id)
        return

admin.site.register(Music, MusicAdmin)