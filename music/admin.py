from django.contrib import admin
from music.models import Music
from player.models import Room
from django.contrib.admin.helpers import ActionForm
from django import forms
import copy

from music.serializers import MusicSerializer

class UpdateActionForm(ActionForm):
    rooms = []
    for room in Room.objects.all():
        new_tuple = (room.name,room.name)
        rooms.append(new_tuple)
    nrroom = forms.ChoiceField(required="false",label=" Target Room for duplication",choices=rooms)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'music_id', 'source', 'duration', 'last_play', 'thumbnail', 'room', 'timer_start','one_shot')
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
        targetRoom = Room.objects.get(name=request.POST['nrroom'])
        if targetRoom:
            for music in queryset:
                if targetRoom.name != music.room.name:
                    if not Music.objects.filter(music_id=music.music_id,room=targetRoom).exists()  :
                        new_entry = Music(count=0,duration=music.duration,last_play=None,music_id=music.music_id,name=music.name,one_shot=False,source=music.source,total_duration=music.total_duration,thumbnail=music.thumbnail,url=music.url)
                        new_entry.room=targetRoom
                        new_entry.save()
            return




admin.site.register(Music, MusicAdmin)
