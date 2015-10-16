# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_auto_20150918_0028'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TemporaryMusic',
        ),
    ]
