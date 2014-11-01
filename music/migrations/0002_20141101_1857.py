# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_initial_room(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Room = apps.get_model("player", "Room")
    Room(name="Amoki's Teamspeak", password="ChangeItLater!").save()


def remove_errored_thumbnails(apps, schema_editor):
    Music = apps.get_model("music", "Music")

    for music in Music.objects.filter(thumbnail__contains="{u'url': u'"):
        # {u'url': u'https://i1.ytimg.com/vi/xchGAzcDNlw/default.jpg', u'width': 120, u'height': 90}
        music.thumbnail = music.thumbnail.split("'")[3]
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_errored_thumbnails),
    ]
