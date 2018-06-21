# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0007_auto_20180620_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='alias',
            field=models.CharField(default=float, unique=True, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variable',
            name='datetype',
            field=models.CharField(default='float', max_length=20),
            preserve_default=False,
        ),
    ]
