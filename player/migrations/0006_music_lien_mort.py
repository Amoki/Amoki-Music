# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20140712_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='lien_mort',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
