# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0019_auto_20150923_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlisttrack',
            name='room',
            field=models.ForeignKey(related_name='playlist', to='player.Room'),
            preserve_default=True,
        ),
    ]
