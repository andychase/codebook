# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_topic_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='path',
            field=models.CharField(max_length='120', default=''),
            preserve_default=False,
        ),
    ]
