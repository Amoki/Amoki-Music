# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20150918_0011'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Source',
        ),
    ]
