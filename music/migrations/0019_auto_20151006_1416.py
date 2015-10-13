# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0018_remove_music_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlisttrack',
            name='room',
            field=models.ForeignKey(related_name='playlist', to='player.Room'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='music',
            name='dead_link',
        ),
        migrations.AlterUniqueTogether(
            name='music',
            unique_together=set([('music_id', 'room')]),
        ),
    ]
