# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0021_https_thumbnails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='thumbnail',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
