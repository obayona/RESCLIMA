# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.search import SearchVector, SearchVectorField      
from django.db import migrations


def index_entries_variables(apps, schema_editor):
    Variable = apps.get_model("timeSeries", "Variable")
    Variable.objects.update(search_vector=SearchVector('name'))

def index_entries_layers(apps, schema_editor):
    Variable = apps.get_model("timeSeries", "Layer")
    Variable.objects.update(search_vector=SearchVector('title','abstract'))


class Migration(migrations.Migration):

    dependencies = [
        ('timeSeries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(index_entries),

        migrations.AlterField(
            model_name='variable',
            name='search_vector',
            field=SearchVectorField(null=False),
        ),
    ]