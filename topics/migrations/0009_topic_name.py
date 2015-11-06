# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topics.models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0008_auto_20150717_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='name',
            field=models.CharField(blank=True, max_length=120, validators=[topics.models.validate_topic_name]),
        ),
    ]
