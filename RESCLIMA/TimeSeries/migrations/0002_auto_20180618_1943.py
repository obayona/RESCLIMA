# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import TimeSeries.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSeries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='readings',
            field=TimeSeries.utils.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='provider',
            name='info',
            field=TimeSeries.utils.fields.JSONField(default=dict),
        ),
    ]
