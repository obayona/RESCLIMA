# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VectorFile',
            new_name='VectorLayer',
        ),
        migrations.RenameField(
            model_name='attribute',
            old_name='vectorfile',
            new_name='vectorlayer',
        ),
        migrations.RenameField(
            model_name='feature',
            old_name='vectorfile',
            new_name='vectorlayer',
        ),
    ]
