# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def transform_to_url(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Music = apps.get_model("player", "Music")
    for music in Music.objects.all():
        music.url = "%s%s" % ("https://www.youtube.com/watch?v=", music.video_id)
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0010_temporarymusic'),
    ]

    operations = [
        migrations.RunPython(transform_to_url)
    ]
