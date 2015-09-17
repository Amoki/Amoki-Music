from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20150426_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('source_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='music.Source')),
            ],
            options={
            },
            bases=('music.source',),
        ),
    ]
