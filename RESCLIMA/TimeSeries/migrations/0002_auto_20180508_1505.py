# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='model',
            field=models.CharField(max_length=50),
        ),
    ]
