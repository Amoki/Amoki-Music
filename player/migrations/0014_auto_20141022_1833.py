from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0013_auto_20141021_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_music',
            field=models.ForeignKey(related_name='+', to='player.Music', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='room',
            name='shuffle',
            field=models.BooleanField(default=False),
        )
    ]
