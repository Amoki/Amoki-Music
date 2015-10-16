# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0019_room_tracks'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='volume',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
    ]
