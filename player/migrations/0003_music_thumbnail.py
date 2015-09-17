from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_remove_music_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='thumbnail',
            field=models.CharField(default='http://i1.ytimg.com/vi/Z0X2FyRl-9s/sddefault.jpg', max_length=255, editable=False),
            preserve_default=False,
        ),
    ]
