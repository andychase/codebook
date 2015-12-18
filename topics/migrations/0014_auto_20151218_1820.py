# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0013_auto_20151218_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='slug',
            field=models.TextField(default=datetime.datetime(2015, 12, 18, 18, 20, 18, 520766, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tags',
            name='text',
            field=models.TextField(),
        ),
    ]
