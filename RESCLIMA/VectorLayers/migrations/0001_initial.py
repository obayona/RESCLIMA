# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Layer', '0001_initial'),
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
            name='VectorLayer',
            fields=[
                ('layer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Layer.Layer')),
                ('filename', models.CharField(max_length=255)),
                ('geom_type', models.CharField(max_length=50)),
                ('encoding', models.CharField(max_length=20)),
            ],
            bases=('Layer.layer',),
        ),
        migrations.AddField(
            model_name='feature',
            name='vectorlayer',
            field=models.ForeignKey(to='VectorLayers.VectorLayer'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='feature',
            field=models.ForeignKey(to='VectorLayers.Feature'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='vectorlayer',
            field=models.ForeignKey(to='VectorLayers.VectorLayer'),
        ),
    ]
