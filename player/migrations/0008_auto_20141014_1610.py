from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20141014_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='lien_mort',
            field=models.BooleanField(default=True),
        ),
    ]
