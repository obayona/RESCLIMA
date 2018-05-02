# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0003_auto_20180426_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vectorlayer',
            name='abstract',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vectorlayer',
            name='encoding',
            field=models.CharField(max_length=20, choices=[(b'ascii', b'ASCII'), (b'latin1', b'Latin-1'), (b'utf8', b'UTF-8')]),
        ),
        migrations.AlterField(
            model_name='vectorlayer',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
