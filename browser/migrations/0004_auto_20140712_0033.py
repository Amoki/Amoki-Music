# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0003_music_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='count',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='music',
            name='playing_date',
        ),
    ]
