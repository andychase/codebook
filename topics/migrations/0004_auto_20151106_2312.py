# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_add_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicsite',
            name='description',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='topicsite',
            name='header',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
