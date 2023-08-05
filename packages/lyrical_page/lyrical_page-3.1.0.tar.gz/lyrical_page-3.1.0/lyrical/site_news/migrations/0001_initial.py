# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteNewsArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('summary', models.CharField(max_length=255, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('publish_date', models.DateTimeField(null=True, blank=True)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteNewsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('url', models.SlugField(unique=True, max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('content', models.TextField(null=True, blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'site news categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sitenewsarticle',
            name='sitenewscategory',
            field=models.ForeignKey(to='site_news.SiteNewsCategory'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sitenewsarticle',
            unique_together=set([('sitenewscategory', 'url')]),
        ),
    ]
