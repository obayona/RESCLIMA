# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0005_auto_20180620_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='frecuency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='station',
            name='token',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
