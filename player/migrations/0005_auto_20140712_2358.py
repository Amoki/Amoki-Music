from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_auto_20140712_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='last_play',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='music',
            name='count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
