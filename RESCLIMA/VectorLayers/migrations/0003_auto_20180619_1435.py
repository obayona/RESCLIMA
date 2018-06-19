# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0002_auto_20180618_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Researcher',
        ),
    ]
