# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_delete_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='source',
            field=models.CharField(max_length=255, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='temporarymusic',
            name='source',
            field=models.CharField(max_length=255, editable=False),
            preserve_default=True,
        ),
    ]
