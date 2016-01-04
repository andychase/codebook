# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0018_auto_20151226_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='icon_content_type',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='icon_data',
            field=models.BinaryField(null=True, blank=True),
        ),
    ]
