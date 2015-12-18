# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('topics', '0009_topic_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.TextField(blank=True)),
                ('title', models.TextField(blank=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now)),
                ('site', models.ForeignKey(to='sites.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LinkVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now)),
                ('link', models.ForeignKey(to='topics.Link')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.TextField()),
                ('text', models.TextField(unique=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TagVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.datetime_safe.datetime.now)),
                ('tag', models.ForeignKey(to='topics.Link')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='topic',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='site',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AlterUniqueTogether(
            name='tagvotes',
            unique_together=set([('user', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='linkvotes',
            unique_together=set([('user', 'link')]),
        ),
    ]
