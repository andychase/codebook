# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0014_auto_20151218_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('slug', models.TextField(unique=True)),
                ('pub_date', models.DateTimeField(default=django.utils.datetime_safe.datetime.now, verbose_name='date published')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.RemoveField(
            model_name='tags',
            name='user',
        ),
        migrations.AlterField(
            model_name='link',
            name='tags',
            field=models.ManyToManyField(to='topics.Tag'),
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
