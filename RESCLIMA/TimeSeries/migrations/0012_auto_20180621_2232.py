# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0011_auto_20180621_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='unit',
            field=models.CharField(max_length=50),
        ),
    ]
