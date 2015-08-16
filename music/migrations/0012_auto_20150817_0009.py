# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_auto_20150428_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='timer_end',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
