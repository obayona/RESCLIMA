# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('abstract', models.TextField(max_length=500, null=True)),
                ('type', models.CharField(max_length=10)),
                ('data_date', models.DateField(null=True, blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('srs_wkt', models.TextField(max_length=500)),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='variables',
            field=models.ManyToManyField(to='Layer.Layer', blank=True),
        ),
    ]
