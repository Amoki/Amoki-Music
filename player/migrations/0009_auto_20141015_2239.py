from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_auto_20141014_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='lien_mort',
        ),
        migrations.AddField(
            model_name='music',
            name='dead_link',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='music',
            name='thumbnail',
            field=models.CharField(max_length=255),
        ),
    ]
