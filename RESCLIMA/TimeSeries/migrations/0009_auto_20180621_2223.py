# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0008_auto_20180621_2223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variable',
            old_name='datetype',
            new_name='datatype',
        ),
    ]
