from django.contrib import admin
from player.models import Room, PlaylistTrack

from ordered_model.admin import OrderedTabularInline


class PlaylistTrackAdmin(OrderedTabularInline):
    model = PlaylistTrack
    fields = ('order', 'move_up_down_links', 'track_type', 'track')
    readonly_fields = ('order', 'move_up_down_links', 'room')
    extra = 0
    ordering = ('track_type', 'order',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shuffle', 'current_music', 'can_adjust_volume')
    inlines = (PlaylistTrackAdmin, )

    def get_urls(self):
        urls = super(RoomAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

admin.site.register(Room, RoomAdmin)
