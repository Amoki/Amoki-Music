from django.contrib import admin, messages
from django.shortcuts import render
from music.models import Music

from music.serializers import MusicSerializer
from music.forms import DuplicateForm


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'music_id', 'source', 'duration', 'last_play', 'thumbnail', 'room', 'timer_start', 'one_shot')
    actions = ('add_music', 'duplicate_music')

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            # Hack to transform music into dict
            music.room.add_music(**MusicSerializer(music).data)
        return

    def duplicate_music(self, request, queryset):
        if 'do_action' in request.POST:

            form = DuplicateForm(request.POST)
            if form.is_valid():

                targetRoom = form.cleaned_data['room']
                for music in queryset:
                    if targetRoom.name != music.room.name:
                        if not Music.objects.filter(music_id=music.music_id, room=targetRoom).exists():
                            new_entry = music
                            new_entry.room = targetRoom
                            new_entry.pk = None
                            new_entry.save()
                messages.success(request, 'Duplication successful')
                return
        else:
            form = DuplicateForm()

        return render(request, 'admin/action_duplicate.html',
            {'title': 'Duplicate music(s) from as room to another',
             'objects': queryset,
             'form': form})
    duplicate_music.short_description = 'Duplicate music'
admin.site.register(Music, MusicAdmin)
