# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0006_auto_20180620_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='frecuency',
            new_name='frequency',
        ),
    ]
