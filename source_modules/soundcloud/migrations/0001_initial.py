from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soundcloud',
            fields=[
                ('source_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='music.Source')),
            ],
            options={
            },
            bases=('music.source',),
        ),
    ]
