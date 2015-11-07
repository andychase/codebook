# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0004_auto_20151106_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicsite',
            name='allow_anonymous_edits',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='topicsite',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
