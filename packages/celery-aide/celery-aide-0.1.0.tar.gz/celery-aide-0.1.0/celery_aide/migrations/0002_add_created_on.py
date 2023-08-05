# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('celery_aide', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='celerytask',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 31, 19, 16, 15, 800337), auto_now_add=True),
            preserve_default=False,
        ),
    ]
