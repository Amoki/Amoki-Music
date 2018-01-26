from __future__ import unicode_literals

from django.db import models, migrations
import player.models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0014_auto_20141022_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='token',
            field=models.CharField(default=player.models.generate_token, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='current_music',
            field=models.ForeignKey(related_name='+', editable=False, to='player.Music', null=True, on_delete=models.CASCADE),
        ),
    ]
