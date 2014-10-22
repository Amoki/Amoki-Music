# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_initial_room(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Room = apps.get_model("player", "Room")
    Room(name="Amoki's Teamspeak", password="ChangeItLater!").save()


def link_all_musics_to_room(apps, schema_editor):
    Music = apps.get_model("player", "Music")
    Room = apps.get_model("player", "Room")

    for music in Music.objects.all():
        music.room = Room.objects.get(name="Amoki's Teamspeak")
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0012_auto_20141018_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(add_initial_room),
        migrations.AddField(
            model_name='music',
            name='room',
            field=models.ForeignKey(null=True, to='player.Room'),
        ),
        migrations.RunPython(link_all_musics_to_room),
        migrations.AlterField(
            model_name='music',
            name='room',
            field=models.ForeignKey(to='player.Room'),
        ),
    ]
