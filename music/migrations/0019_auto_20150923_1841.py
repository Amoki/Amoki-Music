# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0018_remove_music_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='music',
            unique_together=set([('music_id', 'room')]),
        ),
    ]
