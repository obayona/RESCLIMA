# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Layer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='type',
            field=models.CharField(default='shapefile', max_length=10),
            preserve_default=False,
        ),
    ]
