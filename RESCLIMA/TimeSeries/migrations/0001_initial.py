# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField()),
                ('value', models.FloatField()),
            ],
            options={
                'verbose_name': 'Measurement',
                'verbose_name_plural': 'Measurements',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serialNum', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=50, choices=[(b'BLOOMSKY', b'Bloomsky - Sky2'), (b'NIPONCF', b'NEI - CF200'), (b'HOBO', b'Hobo')])),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensors',
            },
        ),
        migrations.CreateModel(
            name='SensorVariable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_sensor', models.ForeignKey(to='TimeSeries.Sensor')),
            ],
            options={
                'verbose_name': 'SensorVariable',
                'verbose_name_plural': 'SensorsVariables',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('unit', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
            },
        ),
        migrations.AddField(
            model_name='sensorvariable',
            name='id_variable',
            field=models.ForeignKey(to='TimeSeries.Variable'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='id_sensorVariable',
            field=models.ForeignKey(to='TimeSeries.SensorVariable'),
        ),
    ]
