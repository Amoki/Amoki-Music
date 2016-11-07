# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 17:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0023_room_nb_shuffle_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='nb_shuffle_items',
            field=models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
