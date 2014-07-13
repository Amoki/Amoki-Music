# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, editable=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('playing_date', models.DateTimeField(null=True)),
                ('duration', models.PositiveIntegerField(editable=False)),
                ('thumbnail', models.CharField(max_length=255, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
