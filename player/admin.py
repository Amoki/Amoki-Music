# -*- coding: utf-8 -*-

from django.contrib import admin
from player.models import Music, Room


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'url', 'duration', 'date', 'last_play', 'dead_link', 'thumbnail')
    actions = ('add_music',)

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            music.room.push(music.url)
        return

admin.site.register(Music, MusicAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shuffle', 'current_music')

admin.site.register(Room, RoomAdmin)
