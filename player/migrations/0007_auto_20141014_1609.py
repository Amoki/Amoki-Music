from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_music_lien_mort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='lien_mort',
            field=models.BooleanField(),
        ),
    ]
