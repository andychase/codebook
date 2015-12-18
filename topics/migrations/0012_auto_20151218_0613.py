# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0011_auto_20151218_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.TextField(unique=True),
        ),
    ]
