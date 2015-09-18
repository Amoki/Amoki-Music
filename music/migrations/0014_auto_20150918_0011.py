# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def save_source(apps, schema_editor):
    Music = apps.get_model("music", "Music")
    for music in Music.objects.all():
        if music.source.pk == 1:
            music.source_old = "youtube"
        else:
            music.source_old = "soundcloud"
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_playlisttrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='source_old',
            field=models.CharField(max_length=255, default="youtube"),
        ),
        migrations.AddField(
            model_name='temporarymusic',
            name='source_old',
            field=models.CharField(max_length=255, default="youtube"),
        ),
        migrations.RunPython(save_source),
        migrations.RemoveField(
            model_name='music',
            name='source',
        ),
        migrations.RemoveField(
            model_name='temporarymusic',
            name='source',
        ),
        migrations.RenameField(
            model_name="music",
            old_name="source_old",
            new_name="source"
        ),
        migrations.RenameField(
            model_name="temporarymusic",
            old_name="source_old",
            new_name="source"
        ),
    ]
