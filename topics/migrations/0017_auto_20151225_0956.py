# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0016_auto_20151221_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='rating_difficulty',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='rating_quality',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='type',
            field=models.TextField(blank=True),
        ),
    ]
