# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('topics', '0007_topicsite_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicSiteData',
            fields=[
                ('site_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='sites.Site')),
                ('css_style', models.TextField(blank=True)),
            ],
            bases=('sites.site',),
        ),
    ]
