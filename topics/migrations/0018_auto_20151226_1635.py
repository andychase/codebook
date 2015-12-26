# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0017_auto_20151225_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.TextField()),
                ('site', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='topics.Source'),
        ),
    ]
