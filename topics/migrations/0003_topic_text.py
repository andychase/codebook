# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20150708_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
