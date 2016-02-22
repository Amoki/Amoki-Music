from django.contrib import admin
from music.models import Music
from player.models import Room
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.db import models

from music.serializers import MusicSerializer

class UpdateActionForm(ActionForm):
    rooms = []
    for room in Room.objects.all():
        tuple = (room.name,room.name)
        rooms.append(tuple)
    nrroom = forms.ChoiceField(required="false",label=" Target Room for duplication",choices=rooms)

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
        nbrroom = request.POST['nrroom']
        roomto = Room.objects.get(name=nbrroom)
        if roomto:
            for music in queryset:
                if roomto.name != music.room.name:
                    new_entry = music
                    new_entry.room=roomto
                    new_entry.id = None
                    new_entry.save()
            return




admin.site.register(Music, MusicAdmin)
