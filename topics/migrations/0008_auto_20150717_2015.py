# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0007_auto_20150709_0321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='name',
            new_name='orig_name',
        ),
        migrations.AlterField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(to='topics.Topic', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
