# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0012_auto_20151218_0613'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='linkvotes',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='linkvotes',
            name='link',
        ),
        migrations.RemoveField(
            model_name='linkvotes',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='tagvotes',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tagvotes',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tagvotes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='ip',
        ),
        migrations.AddField(
            model_name='link',
            name='tags',
            field=models.ManyToManyField(to='topics.Tags'),
        ),
        migrations.DeleteModel(
            name='LinkVotes',
        ),
        migrations.DeleteModel(
            name='TagVotes',
        ),
    ]
