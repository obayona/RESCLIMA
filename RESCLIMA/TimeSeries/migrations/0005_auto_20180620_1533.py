# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0004_auto_20180620_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationtype',
            name='variables',
            field=models.ManyToManyField(to='TimeSeries.Variable', blank=True),
        ),
    ]
