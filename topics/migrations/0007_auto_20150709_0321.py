# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_topic_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='path',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='topic',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now),
        ),
    ]
