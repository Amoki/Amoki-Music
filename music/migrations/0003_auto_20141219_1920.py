# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re


def copy_url_into_video_id(apps, schema_editor):
    Music = apps.get_model("music", "Music")

    for music in Music.objects.all():
        regexVideoId = re.compile("(\?v=|youtu\.be\/)(.{11})", re.IGNORECASE | re.MULTILINE)

        music.music_id = regexVideoId.search(music.url).group(2)
        music.save()


def clear_temporary_music(apps, schema_editor):
    TemporaryMusic = apps.get_model("music", "TemporaryMusic")
    TemporaryMusic.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_20141101_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='music_id',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.RunPython(copy_url_into_video_id),
        migrations.AlterField(
            model_name='music',
            name='music_id',
            field=models.CharField(max_length=16),
        ),
        migrations.RemoveField(
            model_name='music',
            name='url',
        ),
        migrations.RunPython(clear_temporary_music),
        migrations.AddField(
            model_name='temporarymusic',
            name='music_id',
            field=models.CharField(max_length=16)
        ),
        migrations.RemoveField(
            model_name='temporarymusic',
            name='url',
        ),
    ]
