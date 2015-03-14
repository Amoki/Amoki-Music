# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0016_auto_20141101_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='can_adjust_volume',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
