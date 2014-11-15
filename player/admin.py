# -*- coding: utf-8 -*-

from django.contrib import admin
from player.models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shuffle', 'current_music', 'can_adjust_volume')

admin.site.register(Room, RoomAdmin)
