# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0011_auto_20141018_0107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temporarymusic',
            old_name='video_id',
            new_name='url',
        ),
    ]
