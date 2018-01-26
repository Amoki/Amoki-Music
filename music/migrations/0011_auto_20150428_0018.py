from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_auto_20150427_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporarymusic',
            name='source',
            field=models.ForeignKey(editable=False, to='music.Source', on_delete=models.CASCADE),
        ),
    ]
