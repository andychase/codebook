# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topics.models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_squashed_0010_auto_20150717_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='orig_name',
            field=models.CharField(validators=[topics.models.validate_topic_name], max_length=120),
        ),
    ]
