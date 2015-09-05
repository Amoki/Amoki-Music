# -*- coding: utf-8 -*-

from django.contrib import admin
from player.models import Room, PlaylistTrack

from ordered_model.admin import OrderedModelAdmin


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shuffle', 'current_music', 'can_adjust_volume')


class ItemAdmin(OrderedModelAdmin):
    list_display = ('move_up_down_links', 'order', 'track', 'room')

admin.site.register(Room, RoomAdmin)
admin.site.register(PlaylistTrack, ItemAdmin)
