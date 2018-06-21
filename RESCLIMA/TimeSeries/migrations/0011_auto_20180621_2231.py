# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0010_auto_20180621_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='alias',
            field=models.CharField(unique=True, max_length=150),
        ),
    ]
