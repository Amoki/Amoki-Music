# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_auto_20151028_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='duration',
            field=models.PositiveIntegerField(default=models.PositiveIntegerField(editable=False)),
            preserve_default=True,
        ),
    ]
