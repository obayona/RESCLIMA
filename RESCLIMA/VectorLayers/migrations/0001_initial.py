# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField()),
                ('width', models.IntegerField()),
                ('precision', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('attribute', models.ForeignKey(to='VectorLayers.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom_point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('geom_multipoint', django.contrib.gis.db.models.fields.MultiPointField(srid=4326, null=True, blank=True)),
                ('geom_multilinestring', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
                ('geom_multipolygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
                ('geom_geometrycollection', django.contrib.gis.db.models.fields.GeometryCollectionField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VectorFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('srs_wkt', models.TextField(max_length=500)),
                ('geom_type', models.CharField(max_length=50)),
                ('encoding', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='vectorfile',
            field=models.ForeignKey(to='VectorLayers.VectorFile'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='feature',
            field=models.ForeignKey(to='VectorLayers.Feature'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='vectorfile',
            field=models.ForeignKey(to='VectorLayers.VectorFile'),
        ),
    ]
