from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0017_room_can_adjust_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='current_music',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to='music.Music', null=True),
        ),
    ]
