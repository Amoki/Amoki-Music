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
	migrations.AddField(
            model_name='music',
            name='url',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.RunPython(transform_to_url),
        migrations.RemoveField(
            model_name='music',
            name='video_id',
        )
    ]
