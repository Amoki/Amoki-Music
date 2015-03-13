# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20141219_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarymusic',
            name='channel_name',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]