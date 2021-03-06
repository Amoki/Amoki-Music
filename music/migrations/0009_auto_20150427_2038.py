from __future__ import unicode_literals

from django.db import models, migrations


def set_urls(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Music = apps.get_model("music", "Music")
    TemporaryMusic = apps.get_model("music", "TemporaryMusic")
    for music in Music.objects.all():
        music.url = "https://www.youtube.com/watch?v=" + music.music_id
        music.save()
    for tempMusic in TemporaryMusic.objects.all():
        tempMusic.url = "https://www.youtube.com/watch?v=" + tempMusic.music_id
        tempMusic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20150426_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='url',
            field=models.CharField(max_length=512, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='temporarymusic',
            name='url',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.RunPython(set_urls),
        migrations.AlterField(
            model_name='music',
            name='url',
            field=models.CharField(max_length=512, editable=False),
        ),
        migrations.AlterField(
            model_name='temporarymusic',
            name='url',
            field=models.CharField(max_length=512),
        ),
    ]
