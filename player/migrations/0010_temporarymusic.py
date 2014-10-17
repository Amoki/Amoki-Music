# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_auto_20141015_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('duration', models.PositiveIntegerField()),
                ('thumbnail', models.CharField(max_length=255)),
                ('views', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('requestId', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
