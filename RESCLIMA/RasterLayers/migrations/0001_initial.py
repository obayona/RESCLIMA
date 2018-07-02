# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RasterLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=50)),
                ('projected', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50, null=True)),
                ('abstract', models.TextField(max_length=500, null=True)),
                ('data_date', models.DateField(null=True, blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('srs_wkt', models.TextField(max_length=500)),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('numBands', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('rasterlayer', models.ForeignKey(to='RasterLayers.RasterLayer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
