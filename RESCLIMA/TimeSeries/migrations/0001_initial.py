# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
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
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Provider',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serialNum', models.CharField(max_length=30)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Station',
                'verbose_name_plural': 'Station',
            },
        ),
        migrations.CreateModel(
            name='StationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'StationType',
                'verbose_name_plural': 'StationTypes',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=20)),
                ('symbol', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
            },
        ),
        migrations.AddField(
            model_name='station',
            name='stationType',
            field=models.ForeignKey(to='TimeSeries.StationType'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idProvider',
            field=models.ForeignKey(to='TimeSeries.Provider', null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='idStation',
            field=models.ForeignKey(to='TimeSeries.Station', null=True),
        ),
    ]
