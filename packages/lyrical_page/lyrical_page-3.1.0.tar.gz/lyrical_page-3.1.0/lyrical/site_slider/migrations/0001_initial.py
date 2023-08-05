# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('template', models.CharField(help_text=b'Default template path is site_slider/slider.html', max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SliderSlide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, null=True, blank=True)),
                ('image_css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('content_css_class', models.CharField(max_length=255, null=True, blank=True)),
                ('template', models.CharField(help_text=b'Default template path is site_slider/slide.html', max_length=255, null=True, blank=True)),
                ('slider', models.ForeignKey(to='site_slider.Slider')),
            ],
            options={
                'ordering': ('weight',),
            },
            bases=(models.Model,),
        ),
    ]
