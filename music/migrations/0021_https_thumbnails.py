# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_thumbnail_to_https(apps, schema_editor):
    Music = apps.get_model("music", "Music")
    for music in Music.objects.all():
        if music.thumbnail == "http://i1.ytimg.com/vi/Z0X2FyRl-9s/sddefault.jpg":
            music.thumbnail = "https://i1.ytimg.com/vi/Z0X2FyRl-9s/sddefault.jpg"
            music.save()


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_auto_20151028_0925'),
    ]

    operations = [
        migrations.RunPython(default_thumbnail_to_https),
        migrations.AlterField(
            model_name='music',
            name='thumbnail',
            field=models.CharField(default='https://i1.ytimg.com/vi/Z0X2FyRl-9s/sddefault.jpg', max_length=255),
            preserve_default=True,
        ),
    ]
