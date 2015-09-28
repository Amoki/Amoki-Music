from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_playlisttrack'),
        ('player', '0018_auto_20150323_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='tracks',
            field=models.ManyToManyField(related_name=b'+', through='music.PlaylistTrack', to='music.Music'),
            preserve_default=True,
        ),
    ]
