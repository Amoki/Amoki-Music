# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_delete_temporarymusic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='date',
        ),
    ]
