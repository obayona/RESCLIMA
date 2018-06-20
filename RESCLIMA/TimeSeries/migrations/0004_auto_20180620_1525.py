# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0003_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'verbose_name': 'Estation', 'verbose_name_plural': 'Estationes'},
        ),
        migrations.AlterModelOptions(
            name='stationtype',
            options={'verbose_name': 'Tipo de estacion', 'verbose_name_plural': 'Tipo de estaciones'},
        ),
        migrations.AddField(
            model_name='stationtype',
            name='automatic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stationtype',
            name='variables',
            field=models.ManyToManyField(to='TimeSeries.Variable'),
        ),
    ]
