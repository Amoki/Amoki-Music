# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0022_auto_20151218_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='oneShot',
            field=models.BooleanField(default=False),
        ),
    ]
