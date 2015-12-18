# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0010_auto_20151218_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='icon',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.TextField(),
        ),
    ]
