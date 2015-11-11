# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0008_topicsitedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
