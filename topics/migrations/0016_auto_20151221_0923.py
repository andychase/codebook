# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0015_auto_20151218_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='link',
            name='tags',
            field=models.ManyToManyField(blank=True, to='topics.Tag'),
        ),
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='topicsite',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
    ]
