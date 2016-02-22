from django.contrib import admin
from music.models import Music
from player.models import Room
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.db import models

from music.serializers import MusicSerializer

class UpdateActionForm(ActionForm):
    room = models.CharField(choices=Room.objects.all(),)



class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'music_id', 'source', 'duration', 'last_play', 'thumbnail', 'room', 'timer_start')
    actions = ('add_music','duplicate_music')

    action_form = UpdateActionForm
    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            # Hack to transform music into dict
            music.room.add_music(**MusicSerializer(music).data)
        return

    def duplicate_music(self,request,queryset):
        room = request.POST['room']
        for music in queryset:
            room.add_music(**MusicSerializer(music).data)
        return




admin.site.register(Music, MusicAdmin)
