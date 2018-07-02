# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RasterLayers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rasterlayer',
            name='file_format',
            field=models.CharField(default='tif', max_length=10),
            preserve_default=False,
        ),
    ]
