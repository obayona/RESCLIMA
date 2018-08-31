# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.contrib.gis.db.models.fields
import timeSeries.utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id_m', models.IntegerField(serialize=False, primary_key=True)),
                ('ts', models.DateTimeField(default=django.utils.timezone.now)),
                ('readings', timeSeries.utils.fields.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Measurement',
                'verbose_name_plural': 'Measurements',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Proveedor', max_length=120)),
                ('info', timeSeries.utils.fields.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serialNum', models.CharField(max_length=30)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('active', models.BooleanField()),
                ('frequency', models.FloatField(null=True, blank=True)),
                ('token', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Estation',
                'verbose_name_plural': 'Estationes',
            },
        ),
        migrations.CreateModel(
            name='StationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('automatic', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tipo de estacion',
                'verbose_name_plural': 'Tipo de estaciones',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=10)),
                ('alias', models.CharField(unique=True, max_length=150)),
                ('datatype', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
            },
        ),
        migrations.AddField(
            model_name='stationtype',
            name='variables',
            field=models.ManyToManyField(to='timeSeries.Variable', blank=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stationType',
            field=models.ForeignKey(to='timeSeries.StationType'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idProvider',
            field=models.ForeignKey(to='timeSeries.Provider', null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idStation',
            field=models.ForeignKey(to='timeSeries.Station', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('ts', 'id_m')]),
        ),
    ]
