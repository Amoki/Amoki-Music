# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_db(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Source = apps.get_model("music", "Source")
    Source(name="Youtube").save()
    Source(name="Soundcloud").save()


def set_sources_as_youtube(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Music = apps.get_model("music", "Music")
    Source = apps.get_model("music", "Source")
    youtube = Source.objects.get(name="Youtube")
    for music in Music.objects.all():
        music.source = youtube
        music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20150321_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('regex', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(populate_db),
        migrations.AddField(
            model_name='music',
            name='source',
            field=models.ForeignKey(to='music.Source', null=True, editable=False),
            preserve_default=True,
        ),
        migrations.RunPython(set_sources_as_youtube),
        migrations.AlterField(
            model_name='music',
            name='source',
            field=models.ForeignKey(to='music.Source', editable=False),
        ),
    ]
