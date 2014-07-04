from django.contrib import admin
from browser.models import Category, Music, Player


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_id', 'category', 'date')
admin.site.register(Music, MusicAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('actual',)
    actions = ['play_next']

    def play_next(self, request, queryset):
        for player in queryset:
            player.play_next()
            self.message_user(request, "C'est un bon choix...")
    play_next.short_description = "Jouer la musique suivante"

admin.site.register(Player, PlayerAdmin)
