# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_total_duration_as_duration(apps, schema_editor):
    Music = apps.get_model("music", "Music")
    for music in Music.objects.all():
        music.total_duration = music.duration
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0019_auto_20151006_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='total_duration',
            field=models.PositiveIntegerField(editable=False, null=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_total_duration_as_duration),
        migrations.AlterField(
            model_name='music',
            name='total_duration',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='music',
            name='duration',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='music',
            name='timer_end',
        ),
    ]
