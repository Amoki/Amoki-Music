from django.contrib import admin, messages
from django.shortcuts import render
from ordered_model.admin import OrderedModelAdmin
from music.models import Music, Room, MusicQueue
from music.serializers import MusicSerializer
from music.forms import DuplicateForm


class MusicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "count",
        "music_id",
        "service",
        "duration",
        "last_play",
        "thumbnail",
        "room",
        "timer_start",
        "one_shot",
    )
    actions = ("add_music", "duplicate_music")

    def has_add_permission(self, request):
        return False

    def add_music(self, request, queryset):
        for music in queryset:
            # Transform music into dict
            music.room.add_music(music)

    def duplicate_music(self, request, queryset):
        if "do_action" in request.POST:

            form = DuplicateForm(request.POST)
            if form.is_valid():

                targetRoom = form.cleaned_data["room"]
                for music in queryset:
                    if targetRoom.name != music.room.name:
                        if not Music.objects.filter(
                            music_id=music.music_id, room=targetRoom
                        ).exists():
                            new_entry = music
                            new_entry.room = targetRoom
                            new_entry.pk = None
                            new_entry.save()
                messages.success(request, "Duplication successful")
        else:
            form = DuplicateForm()

        return render(
            request,
            "admin/action_duplicate.html",
            {
                "title": "Duplicate music(s) from as room to another",
                "objects": queryset,
                "form": form,
            },
        )

    duplicate_music.short_description = "Duplicate music"


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "shuffle")


class MusicQueueAdmin(OrderedModelAdmin):
    list_display = ("move_up_down_links", "order", "music", "room")


admin.site.register(Room, RoomAdmin)
admin.site.register(MusicQueue, MusicQueueAdmin)
admin.site.register(Music, MusicAdmin)
