# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_music_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='regex',
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=255, editable=False),
        ),
    ]
