# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import VectorLayers.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('VectorLayers', '0005_auto_20180426_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='file_path',
            field=models.FileField(default=datetime.datetime(2018, 5, 4, 21, 6, 27, 41231, tzinfo=utc), upload_to=VectorLayers.models.getFileName),
            preserve_default=False,
        ),
    ]
