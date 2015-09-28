from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20150314_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='timer_end',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='timer_start',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
