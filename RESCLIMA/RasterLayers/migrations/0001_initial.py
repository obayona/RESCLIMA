# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Layer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RasterLayer',
            fields=[
                ('layer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Layer.Layer')),
                ('file_path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=50)),
                ('file_format', models.CharField(max_length=10)),
                ('projected', models.BooleanField(default=True)),
                ('numBands', models.IntegerField(default=1)),
            ],
            bases=('Layer.layer',),
        ),
    ]
