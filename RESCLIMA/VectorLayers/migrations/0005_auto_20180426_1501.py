# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0004_auto_20180426_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vectorlayer',
            name='encoding',
            field=models.CharField(max_length=20),
        ),
    ]
