# -*- coding: utf-8 -*-

from django.contrib import admin
from player.models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shuffle', 'current_music')

admin.site.register(Room, RoomAdmin)
