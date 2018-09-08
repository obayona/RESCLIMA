# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-08 20:14
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import timeSeries.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id_m', models.IntegerField(primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialNum', models.CharField(max_length=30)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('active', models.BooleanField()),
                ('frequency', models.FloatField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Estation',
                'verbose_name_plural': 'Estationes',
            },
        ),
        migrations.CreateModel(
            name='StationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=10)),
                ('alias', models.CharField(max_length=150, unique=True)),
                ('datatype', models.CharField(max_length=20)),
                ('categories', models.ManyToManyField(blank=True, to='search.Category')),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
            },
        ),
        migrations.AddField(
            model_name='stationtype',
            name='variables',
            field=models.ManyToManyField(blank=True, to='timeSeries.Variable'),
        ),
        migrations.AddField(
            model_name='station',
            name='stationType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeSeries.StationType'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idProvider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timeSeries.Provider'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idStation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timeSeries.Station'),
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('ts', 'id_m')]),
        ),
    ]
