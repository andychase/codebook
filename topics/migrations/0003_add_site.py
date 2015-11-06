# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('topics', '0002_auto_20150726_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicSite',
            fields=[
                ('site_ptr', models.OneToOneField(parent_link=True, to='sites.Site', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=120)),
                ('create_date', models.DateTimeField(verbose_name='date created', default=django.utils.datetime_safe.datetime.now)),
            ],
            bases=('sites.site',),
        ),
        migrations.AddField(
            model_name='topic',
            name='site',
            field=models.ForeignKey(to='sites.Site', default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([('site', 'parent', 'name')]),
        ),
    ]
