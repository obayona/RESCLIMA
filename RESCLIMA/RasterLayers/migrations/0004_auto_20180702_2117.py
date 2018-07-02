# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RasterLayers', '0003_auto_20180702_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='rasterlayer',
            field=models.ForeignKey(to='RasterLayers.RasterLayer'),
        ),
    ]
