# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('queue', models.TextField(null=True, blank=True)),
                ('task_id', models.UUIDField()),
                ('state', models.CharField(default='PENDING', max_length=25)),
                ('_args', models.TextField(null=True, blank=True)),
                ('_kwargs', models.TextField(null=True, blank=True)),
                ('_extra', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
