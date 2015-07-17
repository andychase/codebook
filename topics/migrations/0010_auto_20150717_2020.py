# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0009_topic_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([('parent', 'name')]),
        ),
    ]
