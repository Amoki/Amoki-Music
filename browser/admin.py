from django.contrib import admin
from browser.models import Category, Url, Play


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'category', 'date')
admin.site.register(Url, UrlAdmin)


class PlayAdmin(admin.ModelAdmin):
    list_display = ('actual')
