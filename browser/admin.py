from django.contrib import admin
from browser.models import Category, Music


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_id', 'category', 'date')
admin.site.register(Music, MusicAdmin)
