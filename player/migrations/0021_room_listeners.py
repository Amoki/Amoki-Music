# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0020_room_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='listeners',
            field=models.PositiveIntegerField(editable=False, default=0),
            preserve_default=True,
        ),
    ]
