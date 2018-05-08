# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0002_auto_20180421_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='vectorlayer',
            name='abstract',
            field=models.TextField(default=b'No resumen', max_length=500),
        ),
        migrations.AddField(
            model_name='vectorlayer',
            name='centroid',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
        ),
        migrations.AddField(
            model_name='vectorlayer',
            name='data_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vectorlayer',
            name='title',
            field=models.CharField(default=b'No titulo', max_length=50),
        ),
        migrations.AddField(
            model_name='vectorlayer',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 14, 10, 47, 872789, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='style',
            name='vectorlayer',
            field=models.ForeignKey(to='VectorLayers.VectorLayer'),
        ),
    ]
