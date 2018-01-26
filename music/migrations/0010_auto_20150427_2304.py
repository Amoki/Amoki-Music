from __future__ import unicode_literals

from django.db import models, migrations


def set_sources(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Source = apps.get_model("music", "Source")
    TemporaryMusic = apps.get_model("music", "TemporaryMusic")
    youtube = Source.objects.get(name="Youtube")
    for tempMusic in TemporaryMusic.objects.all():
        tempMusic.source = youtube
        tempMusic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_auto_20150427_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarymusic',
            name='source',
            field=models.ForeignKey(to='music.Source', null=True, on_delete=models.CASCADE),
        ),
        migrations.RunPython(set_sources),
        migrations.AlterField(
            model_name='temporarymusic',
            name='source',
            field=models.ForeignKey(to='music.Source', on_delete=models.CASCADE),
        ),
    ]
