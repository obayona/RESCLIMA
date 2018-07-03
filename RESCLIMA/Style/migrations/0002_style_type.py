# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Style', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='type',
            field=models.CharField(default='raster', max_length=10),
            preserve_default=False,
        ),
    ]
