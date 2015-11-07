# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_add_user_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
