from django.contrib import admin
from browser.models import Music


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_id', 'date')
admin.site.register(Music, MusicAdmin)
