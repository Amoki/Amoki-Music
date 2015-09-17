from __future__ import unicode_literals

from django.db import models, migrations


def move_musics(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    MusicOld = apps.get_model("player", "Music")
    MusicNew = apps.get_model("music", "Music")

    for music in MusicOld.objects.all():
        MusicNew(
            id=music.id,
            url=music.url,
            name=music.name,
            date=music.date,
            duration=music.duration,
            thumbnail=music.thumbnail,
            count=music.count,
            last_play=music.last_play,
            dead_link=music.dead_link,
            room=music.room,
        ).save()


def remove_current_music(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Room = apps.get_model("player", "Room")

    for room in Room.objects.all():
        room.current_music = None
        room.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        ('player', '0015_auto_20141031_2339'),
    ]

    operations = [
        migrations.RunPython(remove_current_music),
        migrations.RunPython(move_musics),
        migrations.AlterField(
            model_name='room',
            name='current_music',
            field=models.ForeignKey(related_name=b'+', editable=False, to='music.Music', null=True),
        ),
        migrations.DeleteModel(
            name='Music',
        ),
        migrations.DeleteModel(
            name='TemporaryMusic',
        ),
    ]
