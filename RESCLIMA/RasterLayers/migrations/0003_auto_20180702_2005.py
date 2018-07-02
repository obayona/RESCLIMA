# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RasterLayers', '0002_rasterlayer_file_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rasterlayer',
            name='projected',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='style',
            name='rasterlayer',
            field=models.OneToOneField(to='RasterLayers.RasterLayer'),
        ),
    ]
