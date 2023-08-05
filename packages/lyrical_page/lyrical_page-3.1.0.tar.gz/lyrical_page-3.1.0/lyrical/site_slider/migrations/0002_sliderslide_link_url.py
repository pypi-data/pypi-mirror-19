# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_slider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sliderslide',
            name='link_url',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
