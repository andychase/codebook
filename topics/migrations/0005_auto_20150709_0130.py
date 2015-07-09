# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_topic_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='path',
            field=models.CharField(max_length=120),
        ),
    ]
