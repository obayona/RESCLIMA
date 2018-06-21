# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_auto_20180404_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='shapefile',
            name='srs_wkt',
            field=models.TextField(max_length=500),
        ),
    ]
