from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0015_auto_20141031_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, editable=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('duration', models.PositiveIntegerField(editable=False)),
                ('thumbnail', models.CharField(max_length=255)),
                ('count', models.PositiveIntegerField(default=0, editable=False)),
                ('last_play', models.DateTimeField(null=True)),
                ('dead_link', models.BooleanField(default=False)),
                ('room', models.ForeignKey(to='player.Room', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemporaryMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('duration', models.PositiveIntegerField()),
                ('thumbnail', models.CharField(max_length=255)),
                ('views', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('requestId', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
