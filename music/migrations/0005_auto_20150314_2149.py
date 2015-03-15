# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_temporarymusic_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='timer_end',
            field=models.PositiveIntegerField(null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='music',
            name='timer_start',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=True,
        ),
    ]
