# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=10)),
                ('layers', models.ManyToManyField(to='layer.Layer')),
            ],
        ),
    ]
