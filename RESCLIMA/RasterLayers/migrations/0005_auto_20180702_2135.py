# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RasterLayers', '0004_auto_20180702_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='rasterlayer',
        ),
        migrations.AddField(
            model_name='rasterlayer',
            name='style',
            field=models.ForeignKey(to='RasterLayers.Style', null=True),
        ),
    ]
