from django.contrib import admin
from browser.models import Category, Url, Play


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class UrlAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'date')
admin.site.register(Url, UrlAdmin)


class PlayAdmin(admin.ModelAdmin):
    list_display = ('actual',)
    actions = ['play_next']

    def play_next(self, request, queryset):
        for url in queryset:
            url.play_next()
            self.message_user(request, "C'est un bon choix...")
    play_next.short_description = "Jouer la musique suivante"

admin.site.register(Play, PlayAdmin)
