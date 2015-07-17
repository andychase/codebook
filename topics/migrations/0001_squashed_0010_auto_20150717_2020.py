# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe
import topics.models


class Migration(migrations.Migration):

    replaces = [('topics', '0001_initial'), ('topics', '0002_auto_20150708_2358'), ('topics', '0003_topic_text'), ('topics', '0004_topic_path'), ('topics', '0005_auto_20150709_0130'), ('topics', '0006_topic_parent'), ('topics', '0007_auto_20150709_0321'), ('topics', '0008_auto_20150717_2015'), ('topics', '0009_topic_name'), ('topics', '0010_auto_20150717_2020')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now)),
                ('text', models.TextField(blank=True)),
                ('orig_name', models.CharField(max_length=120)),
                ('parent', models.ForeignKey(null=True, blank=True, to='topics.Topic')),
                ('name', models.CharField(max_length=120, blank=True, validators=[topics.models.validate_special_keywords_name])),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([('parent', 'name')]),
        ),
    ]
